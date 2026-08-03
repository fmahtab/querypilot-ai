import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

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
