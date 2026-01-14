"""GitHub repository handler for uploading repos to s3-agent."""

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import click
from git import Repo

from .uploader import (
    build_tags,
    detect_content_type,
    tagset_has_any,
    upload_file_to_s3_agent,
)


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Parse GitHub URL to extract owner and repo name.
    
    Supports formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - git@github.com:owner/repo.git
    
    Returns:
        Tuple of (owner, repo_name)
    
    Raises:
        ValueError: If URL format is invalid
    """
    # HTTPS format
    https_match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
        url
    )
    if https_match:
        return https_match.group(1), https_match.group(2)
    
    # SSH format
    ssh_match = re.match(
        r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        url
    )
    if ssh_match:
        return ssh_match.group(1), ssh_match.group(2)
    
    raise ValueError(
        f"Invalid GitHub URL format: {url}\n"
        "Expected format: https://github.com/owner/repo or git@github.com:owner/repo.git"
    )


def should_skip_file(file_path: Path, repo_root: Path) -> bool:
    """
    Determine if a file should be skipped during upload.
    
    Skips:
    - .git directory contents
    - Hidden files starting with .
    """
    relative_path = file_path.relative_to(repo_root)
    parts = relative_path.parts
    
    # Skip .git directory
    if ".git" in parts:
        return True
    
    # Skip hidden files
    if any(part.startswith(".") for part in parts):
        return True
    
    return False


def upload_github_repo(
    github_url: str,
    auth_token: str,
    verbose: bool = False,
) -> dict:
    """
    Clone GitHub repo and upload all files to s3-agent with proper tags.
    
    Args:
        github_url: GitHub repository URL
        auth_token: Load account API key
        verbose: Show detailed progress
    
    Returns:
        Dictionary with upload statistics:
        {
            "repo": "owner/repo",
            "files_uploaded": 123,
            "files_skipped": 5,
            "dataitem_ids": ["id1", "id2", ...]
        }
    
    Raises:
        ValueError: If GitHub URL is invalid
        Exception: If cloning or uploading fails
    """
    owner, repo_name = parse_github_url(github_url)
    data_protocol = f"{owner}/{repo_name}"
    
    click.echo(f"Processing GitHub repo: {data_protocol}")

    base_filters = [{"key": "Data-Protocol", "value": data_protocol}]
    if tagset_has_any(base_filters):
        version = 1
        while tagset_has_any(base_filters + [{"key": "Version", "value": str(version)}]):
            version += 1
    else:
        version = 1
    click.echo(f"Using Version={version}")
    
    temp_dir = tempfile.mkdtemp(prefix=f"load-pools-{repo_name}-")
    
    try:
        click.echo("Cloning repository...")
        repo_path = Path(temp_dir) / repo_name
        Repo.clone_from(github_url, repo_path, depth=1)
        
        files_to_upload = []
        for root, dirs, files in os.walk(repo_path):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                
                if should_skip_file(file_path, repo_path):
                    continue
                
                files_to_upload.append(file_path)
        
        click.echo(f"Found {len(files_to_upload)} files to upload")
        
        uploaded_ids = []
        skipped = 0
        
        with click.progressbar(
            files_to_upload,
            label="Uploading files",
            show_pos=True,
        ) as bar:
            for file_path in bar:
                try:
                    relative_path = file_path.relative_to(repo_path)
                    
                    if len(relative_path.parts) > 1:
                        path_str = str(Path(*relative_path.parts[:-1]))
                    else:
                        path_str = ""
                    
                    filename = relative_path.name
                    
                    content_type = detect_content_type(str(file_path))
                    
                    tags = build_tags(
                        data_protocol=data_protocol,
                        filename=filename,
                        path=path_str if path_str else None,
                        content_type=content_type,
                        version=version,
                    )
                    
                    dataitem_id = upload_file_to_s3_agent(
                        file_path=str(file_path),
                        tags=tags,
                        auth_token=auth_token,
                        content_type=content_type,
                    )
                    
                    uploaded_ids.append(dataitem_id)
                    
                    if verbose:
                        click.echo(f"  OK {relative_path} -> {dataitem_id}")
                
                except Exception as e:
                    skipped += 1
                    if verbose:
                        click.echo(f"  SKIP {relative_path}: {e}", err=True)
        
        click.echo("Upload complete.")
        click.echo(f"  Files uploaded: {len(uploaded_ids)}")
        if skipped > 0:
            click.echo(f"  Files skipped: {skipped}")
        
        return {
            "repo": data_protocol,
            "files_uploaded": len(uploaded_ids),
            "files_skipped": skipped,
            "dataitem_ids": uploaded_ids,
        }
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
