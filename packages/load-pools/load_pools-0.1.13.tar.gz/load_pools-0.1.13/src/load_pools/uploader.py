"""Upload utilities for s3-agent."""

import json
import mimetypes
import os
from pathlib import Path
from typing import Dict, List, Optional

import requests


DEFAULT_AGENT_URL = "https://load-s3-agent.load.network/upload"
TAGS_QUERY_URL = "https://load-s3-agent.load.network/tags/query"


def detect_content_type(file_path: str) -> str:
    """Detect MIME type for a file."""
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def upload_file_to_s3_agent(
    file_path: str,
    tags: List[Dict[str, str]],
    auth_token: str,
    agent_url: str = DEFAULT_AGENT_URL,
    content_type: Optional[str] = None,
    return_response: bool = False,
) -> str:
    """
    Upload a single file to s3-agent with tags.
    
    Args:
        file_path: Path to the file to upload
        tags: List of tag dictionaries with 'key' and 'value' fields
        auth_token: Load account API key
        agent_url: s3-agent upload endpoint
        content_type: MIME type (auto-detected if None)
    
    Returns:
        dataitem_id from the s3-agent response
    
    Raises:
        requests.RequestException: If upload fails
        KeyError: If response doesn't contain dataitem_id
    """
    if content_type is None:
        content_type = detect_content_type(file_path)
    
    filename = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        files = {
            "file": (filename, f, content_type)
        }
        
        data = {
            "content_type": content_type,
            "tags": json.dumps(tags),
        }
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
        }
        
        response = requests.post(
            agent_url,
            headers=headers,
            files=files,
            data=data,
        )
        
        response.raise_for_status()
        result = response.json()
        
        if return_response:
            return result
        return result["dataitem_id"]


def build_tags(
    data_protocol: str,
    filename: str,
    path: Optional[str] = None,
    content_type: Optional[str] = None,
    extra_tags: Optional[Dict[str, str]] = None,
    version: Optional[int] = None,
) -> List[Dict[str, str]]:
    """
    Build standardized tags for a file upload.
    
    Args:
        data_protocol: The Data-Protocol value (e.g., "username/reponame")
        filename: Just the filename (e.g., "9582.png")
        path: Folder path (e.g., "images/grayscale")
        content_type: MIME type
        extra_tags: Additional custom tags
    
    Returns:
        List of tag dictionaries
    """
    tags = [
        {"key": "Data-Protocol", "value": data_protocol},
        {"key": "Filename", "value": filename},
    ]
    
    if path:
        tags.append({"key": "Path", "value": path})
    
    if content_type:
        tags.append({"key": "Content-Type", "value": content_type})
    
    if extra_tags:
        for key, value in extra_tags.items():
            tags.append({"key": key, "value": value})

    if version is not None:
        tags.append({"key": "Version", "value": str(version)})
    
    return tags


def tags_query(
    filters: List[Dict[str, str]],
    query_url: str = TAGS_QUERY_URL,
) -> Dict:
    response = requests.post(
        query_url,
        headers={"Content-Type": "application/json"},
        json={"filters": filters},
    )
    response.raise_for_status()
    return response.json()


def tagset_has_any(filters: List[Dict[str, str]]) -> bool:
    data = tags_query(filters)
    if isinstance(data, list):
        return len(data) > 0
    if isinstance(data, dict):
        for key in ("dataitems", "items", "results", "data"):
            if key in data and isinstance(data[key], list):
                return len(data[key]) > 0
        if "count" in data:
            try:
                return int(data["count"]) > 0
            except (TypeError, ValueError):
                return bool(data["count"])
    return bool(data)
