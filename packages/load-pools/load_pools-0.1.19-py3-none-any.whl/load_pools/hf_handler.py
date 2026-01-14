"""HuggingFace dataset handler."""

import json
import os
import tempfile
from typing import Any, Callable, Dict, Iterable, Optional

import click
import requests

from .uploader import upload_file_to_s3_agent

HF_DATASETS_SERVER = "https://datasets-server.huggingface.co"
ROWS_PAGE_SIZE = 100


def _hf_headers(hf_token: Optional[str]) -> Dict[str, str]:
    token = hf_token or os.environ.get("HF_TOKEN")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _fetch_json(url: str, hf_token: Optional[str]) -> Dict[str, Any]:
    response = requests.get(url, headers=_hf_headers(hf_token))
    response.raise_for_status()
    return response.json()


def _fetch_configs(dataset: str, hf_token: Optional[str]) -> Iterable[str]:
    url = f"{HF_DATASETS_SERVER}/splits?dataset={dataset}"
    data = _fetch_json(url, hf_token)
    return sorted({split["config"] for split in data.get("splits", [])})


def _fetch_dataset_info(dataset: str, config: str, hf_token: Optional[str]) -> Dict[str, Any]:
    url = f"{HF_DATASETS_SERVER}/info?dataset={dataset}&config={config}"
    data = _fetch_json(url, hf_token)
    return data.get("dataset_info", {})


def _fetch_dataset_rows(
    dataset: str,
    config: str,
    split: str,
    offset: int,
    limit: int,
    hf_token: Optional[str],
) -> Dict[str, Any]:
    url = (
        f"{HF_DATASETS_SERVER}/rows?dataset={dataset}"
        f"&config={config}&split={split}&offset={offset}&limit={limit}"
    )
    return _fetch_json(url, hf_token)


def _build_row_tags(
    dataset: str,
    config: str,
    split: str,
    row_id: str,
    split_info: Optional[Dict[str, Any]],
    extra_tags: Optional[dict],
    version: int,
    job_hash: str,
) -> list[dict[str, str]]:
    tags = [
        {"key": "Data-Protocol", "value": dataset},
        {"key": "hf-dataset", "value": dataset},
        {"key": "config", "value": config},
        {"key": "split", "value": split},
        {"key": "id", "value": row_id},
        {"key": "content-type", "value": "application/json"},
        {"key": "Job-Hash", "value": job_hash},
    ]

    if split_info and split_info.get("num_examples"):
        tags.append({"key": "split-total-rows", "value": str(split_info["num_examples"])})

    if extra_tags:
        for key, value in extra_tags.items():
            tags.append({"key": key, "value": str(value)})

    tags.append({"key": "Version", "value": str(version)})

    return tags


def _upload_row(
    row_data: Dict[str, Any],
    *,
    dataset: str,
    config: str,
    split: str,
    row_id: str,
    split_info: Optional[Dict[str, Any]],
    auth_token: str,
    extra_tags: Optional[dict],
    version: int,
    job_hash: str,
    verbose: bool,
) -> str:
    tags = _build_row_tags(
        dataset,
        config,
        split,
        row_id,
        split_info,
        extra_tags,
        version,
        job_hash,
    )
    if verbose:
        click.echo(f"  TAGS {row_id}: {json.dumps(tags, ensure_ascii=True)}")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(row_data, tmp, ensure_ascii=True)
        tmp_path = tmp.name

    try:
        response = upload_file_to_s3_agent(
            file_path=tmp_path,
            tags=tags,
            auth_token=auth_token,
            content_type="application/json",
            return_response=verbose,
        )
        if verbose:
            click.echo(f"  RESP {row_id}: {json.dumps(response, ensure_ascii=True)}")
            return response["dataitem_id"]
        return response
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def upload_huggingface_dataset(
    repo_id: str,
    auth_token: str,
    extra_tags: Optional[dict] = None,
    hf_token: Optional[str] = None,
    verbose: bool = False,
    job_hash: str | None = None,
    version: int | None = None,
    record_dataitem: Callable[[str], None] | None = None,
) -> dict:
    click.echo(f"Processing HuggingFace repo: {repo_id}")
    if version is None or not job_hash:
        raise ValueError("job_hash and version are required for uploads")
    configs = _fetch_configs(repo_id, hf_token)
    if not configs:
        raise ValueError(f"No configs found for dataset {repo_id}")

    total_uploaded = 0
    total_skipped = 0
    uploaded_ids = []

    for config in configs:
        dataset_info = _fetch_dataset_info(repo_id, config, hf_token)
        splits = dataset_info.get("splits", {})
        if not splits:
            click.echo(f"No splits found for config {config}")
            continue

        for split_name, split_info in splits.items():
            click.echo(f"Uploading {repo_id} config={config} split={split_name}")
            if version is not None:
                click.echo(f"Using Version={version}")
            total_rows = None
            if isinstance(split_info, dict):
                total_rows = split_info.get("num_examples")
                if isinstance(total_rows, int) and total_rows > 0:
                    click.echo(f"Total rows: {total_rows}")
            offset = 0
            id_field = None
            batch_num = 1
            bar = None
            bar_started = False
            if isinstance(total_rows, int) and total_rows > 0:
                bar = click.progressbar(length=total_rows, label="Uploading rows")

            try:
                while True:
                    data = _fetch_dataset_rows(
                        repo_id,
                        config,
                        split_name,
                        offset,
                        ROWS_PAGE_SIZE,
                        hf_token,
                    )
                    rows = data.get("rows", [])
                    if not rows:
                        break

                    if id_field is None:
                        id_field = next(iter(rows[0]["row"].keys()), None)
                        if not id_field:
                            raise ValueError(f"Could not determine id field for {repo_id}")
                        click.echo(f"Using id field: {id_field}")
                        click.echo("")
                        if bar is not None and not bar_started:
                            bar.__enter__()
                            bar_started = True

                    if bar is None:
                        click.echo(f"Batch {batch_num}")
                        with click.progressbar(
                            rows,
                            label="Uploading rows",
                            show_pos=True,
                        ) as batch_bar:
                            for row in batch_bar:
                                row_data = row.get("row", {})
                                row_id = str(row_data.get(id_field, ""))
                                if not row_id:
                                    total_skipped += 1
                                    continue
                                try:
                                    dataitem_id = _upload_row(
                                        row_data,
                                        dataset=repo_id,
                                        config=config,
                                        split=split_name,
                                        row_id=row_id,
                                        split_info=split_info,
                                        auth_token=auth_token,
                                        extra_tags=extra_tags,
                                        version=version,
                                        job_hash=job_hash or "",
                                        verbose=verbose,
                                    )
                                    uploaded_ids.append(dataitem_id)
                                    total_uploaded += 1
                                    if record_dataitem:
                                        record_dataitem(dataitem_id)
                                except Exception as exc:
                                    total_skipped += 1
                                    click.echo(f"  SKIP {row_id}: {exc}", err=True)
                        batch_num += 1
                    else:
                        for row in rows:
                            row_data = row.get("row", {})
                            row_id = str(row_data.get(id_field, ""))
                            if not row_id:
                                total_skipped += 1
                                bar.update(1)
                                continue
                            try:
                                dataitem_id = _upload_row(
                                    row_data,
                                    dataset=repo_id,
                                    config=config,
                                    split=split_name,
                                    row_id=row_id,
                                    split_info=split_info,
                                    auth_token=auth_token,
                                    extra_tags=extra_tags,
                                    version=version,
                                    job_hash=job_hash or "",
                                    verbose=verbose,
                                )
                                uploaded_ids.append(dataitem_id)
                                total_uploaded += 1
                                if record_dataitem:
                                    record_dataitem(dataitem_id)
                            except Exception as exc:
                                total_skipped += 1
                                click.echo(f"  SKIP {row_id}: {exc}", err=True)
                            bar.update(1)

                    if len(rows) < ROWS_PAGE_SIZE:
                        break
                    offset += ROWS_PAGE_SIZE
            finally:
                if bar is not None and bar_started:
                    bar.__exit__(None, None, None)

    click.echo("Upload complete.")
    click.echo(f"  Files uploaded: {total_uploaded}")
    if total_skipped > 0:
        click.echo(f"  Files skipped: {total_skipped}")

    return {
        "repo": repo_id,
        "files_uploaded": total_uploaded,
        "files_skipped": total_skipped,
        "dataitem_ids": uploaded_ids,
    }
