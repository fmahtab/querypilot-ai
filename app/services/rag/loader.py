import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
import boto3

FRONT_MATTER_PATTERN = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n",
    re.DOTALL,
)


def _normalize_metadata_value(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _normalize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return {key: _normalize_metadata_value(val) for key, val in metadata.items()}


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        return {}, text

    raw: dict[str, Any] = yaml.safe_load(match.group(1)) or {}
    metadata = _normalize_metadata(raw)
    body = text[match.end() :]
    return metadata, body


def load_markdown_file(path: Path) -> tuple[str, dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    return path.name, metadata, body


def load_all_markdown_files(docs_dir: Path) -> list[tuple[str, dict[str, Any], str]]:
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    return [
        load_markdown_file(path)
        for path in sorted(docs_dir.glob("*.md"))
    ]

def load_markdown_from_s3(s3_client, bucket: str, key: str) -> tuple[str, dict[str, Any], str]:
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    text = resp["Body"].read().decode("utf-8")
    text = text.replace("\r\n", "\n")  # match read_text() behavior on Windows
    metadata, body = parse_front_matter(text)
    filename = key.rsplit("/", 1)[-1]  # "retailstar_docs/returns_policy.md" -> "returns_policy.md"
    return filename, metadata, body


def load_all_markdown_from_s3(
    bucket: str,
    prefix: str,
    region: str = "us-east-2",
    s3_client=None,
) -> list[tuple[str, dict[str, Any], str]]:
    s3 = s3_client or boto3.client("s3", region_name=region)

    keys: list[str] = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".md"):
                keys.append(obj["Key"])

    if not keys:
        raise FileNotFoundError(f"No .md files found in s3://{bucket}/{prefix}")

    return [load_markdown_from_s3(s3, bucket, key) for key in sorted(keys)]