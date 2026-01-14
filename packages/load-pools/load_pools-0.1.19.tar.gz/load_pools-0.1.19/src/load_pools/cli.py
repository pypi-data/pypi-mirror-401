"""CLI interface for load-pools."""

import sys
import time
import uuid
from pathlib import Path

import click

from .github_handler import parse_github_url, upload_github_repo
from .hf_handler import upload_huggingface_dataset
from .uploader import (
    build_job_summary_tags,
    next_version,
    upload_file_to_s3_agent,
    write_job_summary,
)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option("0.1.19", "-v", "--version", prog_name="load-pools")
def cli():
    """
    Load Pools CLI - Upload HuggingFace datasets and GitHub repos to Load S3.

    create:

      load-pools create --auth <LOAD_ACC> --hugging-face <HF_SLUG>

      load-pools create --auth <LOAD_ACC> --github <REPO_URL>

      Create a load_acc key at cloud.load.network.

      --hugging-face expects a dataset slug like openai/graphwalks

      --github expects a base repository URL like https://github.com/user/repo
    """
    pass


@cli.command()
@click.option(
    "--github",
    "github_url",
    type=str,
    help="GitHub repository URL (e.g., https://github.com/owner/repo)",
)
@click.option(
    "--hugging-face",
    "huggingface_repo",
    type=str,
    help="HuggingFace repository slug (e.g., username/dataset-name)",
)
@click.option(
    "--load-auth",
    "--auth",
    "auth_token",
    required=True,
    type=str,
    help="Load account API key (LOAD_ACC)",
)
@click.option(
    "--hf-auth",
    "hf_token",
    required=False,
    type=str,
    help="HuggingFace access token (HF_TOKEN)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed upload progress",
)
def create(github_url, huggingface_repo, auth_token, hf_token, verbose):
    """
    Create a new pool by uploading a GitHub repo or HuggingFace dataset.

    load-pools create --auth <LOAD_ACC> --hugging-face <HF_SLUG>
    load-pools create --auth <LOAD_ACC> --github <REPO_URL>

    Create a load_acc key at cloud.load.network.

    --hugging-face expects a dataset slug like openai/graphwalks

    --github expects a base repository URL like https://github.com/user/repo
    """
    sources = [github_url, huggingface_repo]
    provided_sources = [s for s in sources if s is not None]
    
    if len(provided_sources) == 0:
        click.echo("Error: Must provide either --github or --hugging-face", err=True)
        click.echo("Run 'load-pools create --help' for usage information.", err=True)
        sys.exit(1)
    
    if len(provided_sources) > 1:
        click.echo("Error: Cannot specify both --github and --hugging-face", err=True)
        click.echo("Please provide only one source.", err=True)
        sys.exit(1)
    
    data_protocol = None
    if github_url:
        owner, repo_name = parse_github_url(github_url)
        data_protocol = f"{owner}/{repo_name}"
    elif huggingface_repo:
        data_protocol = huggingface_repo

    job_hash = uuid.uuid4().hex
    created_at = int(time.time())
    version = next_version([{"key": "Data-Protocol", "value": data_protocol}])
    job_filename = f"{data_protocol.replace('/', '_')}_{job_hash}.json"
    job_path = str(Path.cwd() / job_filename)
    dataitems = []

    def record_dataitem(dataitem_id: str) -> None:
        dataitems.append(dataitem_id)
        write_job_summary(
            job_path,
            data_protocol=data_protocol,
            job_hash=job_hash,
            version=version,
            created_at=created_at,
            dataitems=dataitems,
        )

    write_job_summary(
        job_path,
        data_protocol=data_protocol,
        job_hash=job_hash,
        version=version,
        created_at=created_at,
        dataitems=dataitems,
    )

    try:
        if github_url:
            result = upload_github_repo(
                github_url=github_url,
                auth_token=auth_token,
                verbose=verbose,
                job_hash=job_hash,
                version=version,
                record_dataitem=record_dataitem,
            )
            
            click.echo(f"\nSuccess. Repository '{result['repo']}' uploaded to Load S3")
            click.echo(f"   Files uploaded: {result['files_uploaded']}")
            if result['files_skipped'] > 0:
                click.echo(f"   Files skipped: {result['files_skipped']}")
            
            click.echo("\nQuery uploaded files with:")
            click.echo(f'   curl -X POST https://load-s3-agent.load.network/tags/query \\')
            click.echo(f'     -H "Content-Type: application/json" \\')
            click.echo(f'     -d \'{{"filters": [{{"key": "Data-Protocol", "value": "{result["repo"]}"}}]}}\'')
        
        elif huggingface_repo:
            result = upload_huggingface_dataset(
                repo_id=huggingface_repo,
                auth_token=auth_token,
                hf_token=hf_token,
                verbose=verbose,
                job_hash=job_hash,
                version=version,
                record_dataitem=record_dataitem,
            )
            
            click.echo(f"\nSuccess. HuggingFace repo '{result['repo']}' uploaded to Load S3")
            click.echo(f"   Files uploaded: {result['files_uploaded']}")
            if result['files_skipped'] > 0:
                click.echo(f"   Files skipped: {result['files_skipped']}")

        summary_tags = build_job_summary_tags(
            data_protocol=data_protocol,
            job_hash=job_hash,
            version=version,
            created_at=created_at,
        )
        summary_dataitem_id = upload_file_to_s3_agent(
            file_path=job_path,
            tags=summary_tags,
            auth_token=auth_token,
            content_type="application/json",
        )
        click.echo(f"\nJob summary uploaded: {summary_dataitem_id}")
        click.echo(f"Summary file: {job_filename}")
    
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
