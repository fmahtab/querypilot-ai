import tempfile
import unittest
from pathlib import Path

from app.services.rag import ingest_retailstar_docs
from app.services.rag.chunker import chunk_by_headings
from app.services.rag.loader import load_all_markdown_files, load_markdown_file, parse_front_matter


SAMPLE_DOC = """\
---
title: Sample Policy
tags: [inventory, policy]
department: Merchandising & Operations
document_type: Inventory Policy
version: 1.0
last_updated: 2026-08-03
---

# Sample Policy

Intro under title.

---

## Stock Levels

| Status | Definition |
|--------|------------|
| Low Inventory | Below minimum threshold |

### Low inventory

A SKU is flagged as **low inventory** when:

```
on_hand_quantity < minimum_threshold
```

Alerts are sent to the store manager.

### Maximum thresholds

Maximum on-hand quantities are set at **3× the minimum threshold**.

---

## Replenishment Rules

### Automatic reorder

Reorder quantity is calculated as:

```
maximum_threshold - on_hand_quantity
```
"""


class TestFrontMatterParsing(unittest.TestCase):
    def test_parses_yaml_front_matter(self) -> None:
        metadata, body = parse_front_matter(SAMPLE_DOC)

        self.assertEqual(metadata["title"], "Sample Policy")
        self.assertEqual(metadata["tags"], ["inventory", "policy"])
        self.assertEqual(metadata["department"], "Merchandising & Operations")
        self.assertEqual(metadata["document_type"], "Inventory Policy")
        self.assertEqual(metadata["version"], 1.0)
        self.assertEqual(metadata["last_updated"], "2026-08-03")
        self.assertTrue(body.startswith("# Sample Policy"))

    def test_returns_empty_metadata_when_front_matter_missing(self) -> None:
        metadata, body = parse_front_matter("# Title\n\nBody text.")

        self.assertEqual(metadata, {})
        self.assertEqual(body, "# Title\n\nBody text.")


class TestLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_discovers_markdown_files_in_sorted_order(self) -> None:
        (self.docs_dir / "b_doc.md").write_text("# B\n", encoding="utf-8")
        (self.docs_dir / "a_doc.md").write_text("# A\n", encoding="utf-8")

        loaded = load_all_markdown_files(self.docs_dir)

        self.assertEqual([name for name, _, _ in loaded], ["a_doc.md", "b_doc.md"])

    def test_load_markdown_file_returns_filename_metadata_and_body(self) -> None:
        path = self.docs_dir / "sample.md"
        path.write_text(SAMPLE_DOC, encoding="utf-8")

        source_file, metadata, body = load_markdown_file(path)

        self.assertEqual(source_file, "sample.md")
        self.assertEqual(metadata["title"], "Sample Policy")
        self.assertIn("# Sample Policy", body)
        self.assertNotIn("title: Sample Policy", body)

    def test_raises_when_docs_directory_missing(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_all_markdown_files(self.docs_dir / "missing")


class TestChunker(unittest.TestCase):
    def test_splits_on_all_heading_levels(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)

        headings = [chunk["heading"] for chunk in chunks]
        self.assertEqual(
            headings,
            [
                "Sample Policy",
                "Stock Levels",
                "Low inventory",
                "Maximum thresholds",
                "Replenishment Rules",
                "Automatic reorder",
            ],
        )

    def test_includes_heading_line_in_chunk_content(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        low_inventory = next(chunk for chunk in chunks if chunk["heading"] == "Low inventory")

        self.assertTrue(low_inventory["content"].startswith("### Low inventory"))

    def test_preserves_fenced_code_blocks(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        low_inventory = next(chunk for chunk in chunks if chunk["heading"] == "Low inventory")

        self.assertIn("```\non_hand_quantity < minimum_threshold\n```", low_inventory["content"])

    def test_preserves_tables(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        stock_levels = next(chunk for chunk in chunks if chunk["heading"] == "Stock Levels")

        self.assertIn("| Status | Definition |", stock_levels["content"])
        self.assertIn("| Low Inventory | Below minimum threshold |", stock_levels["content"])

    def test_preserves_horizontal_rules_in_section_content(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        title_chunk = chunks[0]

        self.assertIn("---", title_chunk["content"])

    def test_builds_nested_section_paths(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        low_inventory = next(chunk for chunk in chunks if chunk["heading"] == "Low inventory")
        automatic_reorder = next(chunk for chunk in chunks if chunk["heading"] == "Automatic reorder")

        self.assertEqual(
            low_inventory["section_path"],
            ["Sample Policy", "Stock Levels", "Low inventory"],
        )
        self.assertEqual(
            automatic_reorder["section_path"],
            ["Sample Policy", "Replenishment Rules", "Automatic reorder"],
        )

    def test_sets_heading_levels(self) -> None:
        _, body = parse_front_matter(SAMPLE_DOC)
        chunks = chunk_by_headings(body)
        chunks_by_heading = {chunk["heading"]: chunk for chunk in chunks}

        self.assertEqual(chunks_by_heading["Sample Policy"]["heading_level"], 1)
        self.assertEqual(chunks_by_heading["Stock Levels"]["heading_level"], 2)
        self.assertEqual(chunks_by_heading["Low inventory"]["heading_level"], 3)


class TestIngestion(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.temp_dir.name)
        (self.docs_dir / "sample.md").write_text(SAMPLE_DOC, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_ingest_returns_document_chunks(self) -> None:
        chunks = ingest_retailstar_docs(docs_dir=self.docs_dir)

        self.assertGreater(len(chunks), 0)
        self.assertTrue(all(chunk.chunk_id for chunk in chunks))
        self.assertTrue(all(chunk.content for chunk in chunks))

    def test_chunk_ids_are_unique_and_deterministic(self) -> None:
        first_run = ingest_retailstar_docs(docs_dir=self.docs_dir)
        second_run = ingest_retailstar_docs(docs_dir=self.docs_dir)

        first_ids = [chunk.chunk_id for chunk in first_run]
        second_ids = [chunk.chunk_id for chunk in second_run]

        self.assertEqual(len(first_ids), len(set(first_ids)))
        self.assertEqual(first_ids, second_ids)
        self.assertEqual(first_ids[0], "sample.md::chunk-000")

    def test_metadata_preserves_front_matter_and_derived_fields(self) -> None:
        chunks = ingest_retailstar_docs(docs_dir=self.docs_dir)
        low_inventory = next(
            chunk for chunk in chunks if chunk.metadata["heading"] == "Low inventory"
        )

        self.assertEqual(low_inventory.metadata["title"], "Sample Policy")
        self.assertEqual(low_inventory.metadata["source_file"], "sample.md")
        self.assertEqual(low_inventory.metadata["heading"], "Low inventory")
        self.assertEqual(low_inventory.metadata["heading_level"], 3)
        self.assertEqual(
            low_inventory.metadata["section_path"],
            ["Sample Policy", "Stock Levels", "Low inventory"],
        )
        self.assertIsInstance(low_inventory.metadata["chunk_index"], int)

    def test_ingest_from_real_docs_directory(self) -> None:
        real_docs_dir = Path("data/retailstar_docs")
        if not real_docs_dir.is_dir():
            self.skipTest("RetailStar docs directory not available")

        chunks = ingest_retailstar_docs(docs_dir=real_docs_dir)
        source_files = {chunk.metadata["source_file"] for chunk in chunks}

        self.assertGreater(len(chunks), 0)
        self.assertIn("company_overview.md", source_files)
        self.assertIn("inventory_policy.md", source_files)
        self.assertEqual(len(chunks), len({chunk.chunk_id for chunk in chunks}))


if __name__ == "__main__":
    unittest.main()
