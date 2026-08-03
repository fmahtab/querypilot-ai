import re
from typing import Any

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def chunk_by_headings(body: str) -> list[dict[str, Any]]:
    matches = list(HEADING_PATTERN.finditer(body))
    if not matches:
        content = body.strip()
        if not content:
            return []
        return [
            {
                "heading": "",
                "heading_level": 0,
                "section_path": [],
                "content": content,
            }
        ]

    chunks: list[dict[str, Any]] = []
    section_stack: list[tuple[int, str]] = []

    for index, match in enumerate(matches):
        level = len(match.group(1))
        heading_text = match.group(2).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)

        while section_stack and section_stack[-1][0] >= level:
            section_stack.pop()
        section_stack.append((level, heading_text))

        chunks.append(
            {
                "heading": heading_text,
                "heading_level": level,
                "section_path": [title for _, title in section_stack],
                "content": body[start:end].rstrip(),
            }
        )

    return chunks
