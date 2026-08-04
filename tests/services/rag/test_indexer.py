import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.schemas.rag import DocumentChunk
from app.services.rag.indexer import index_retailstar_docs


SAMPLE_DOC = """\
---
title: Sample Policy
version: 1.0
last_updated: 2026-08-03
---

# Sample Policy

## Purpose

Purpose text.
"""


class TestIndexer(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.temp_dir.name)
        (self.docs_dir / "sample.md").write_text(SAMPLE_DOC, encoding="utf-8")
        self.mock_db = MagicMock()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @patch("app.services.rag.indexer.replace_all_chunks")
    @patch("app.services.rag.indexer.embed_chunks")
    @patch("app.services.rag.indexer.ingest_retailstar_docs")
    def test_orchestrates_ingest_embed_then_replace_workflow(
        self,
        mock_ingest: MagicMock,
        mock_embed: MagicMock,
        mock_replace: MagicMock,
    ) -> None:
        chunks = [
            DocumentChunk(
                chunk_id="sample.md::chunk-000",
                content="# Sample Policy",
                metadata={"title": "Sample Policy", "source_file": "sample.md"},
            ),
            DocumentChunk(
                chunk_id="sample.md::chunk-001",
                content="## Purpose\n\nPurpose text.",
                metadata={"title": "Sample Policy", "source_file": "sample.md"},
            ),
        ]
        embeddings = [[0.1, 0.2], [0.3, 0.4]]
        call_order: list[str] = []

        mock_ingest.side_effect = lambda docs_dir: call_order.append("ingest") or chunks
        mock_embed.side_effect = lambda ingested: call_order.append("embed") or embeddings
        mock_replace.side_effect = (
            lambda db, ingested, embeds, model: call_order.append("replace") or 2
        )

        result = index_retailstar_docs(docs_dir=self.docs_dir, db=self.mock_db)

        self.assertEqual(call_order, ["ingest", "embed", "replace"])
        mock_ingest.assert_called_once_with(self.docs_dir)
        mock_embed.assert_called_once_with(chunks)
        mock_replace.assert_called_once_with(
            self.mock_db,
            chunks,
            embeddings,
            settings.openai_embedding_model,
        )
        self.assertEqual(result.chunk_count, 2)

    @patch("app.services.rag.indexer.replace_all_chunks")
    @patch("app.services.rag.indexer.embed_chunks")
    @patch("app.services.rag.indexer.ingest_retailstar_docs")
    def test_preserves_existing_index_when_no_chunks_found(
        self,
        mock_ingest: MagicMock,
        mock_embed: MagicMock,
        mock_replace: MagicMock,
    ) -> None:
        mock_ingest.return_value = []

        result = index_retailstar_docs(docs_dir=self.docs_dir, db=self.mock_db)

        mock_embed.assert_not_called()
        mock_replace.assert_not_called()
        self.assertEqual(result.chunk_count, 0)

    @patch("app.services.rag.indexer.replace_all_chunks")
    @patch("app.services.rag.indexer.embed_chunks")
    def test_indexes_ingested_documents_end_to_end_with_mocks(
        self,
        mock_embed: MagicMock,
        mock_replace: MagicMock,
    ) -> None:
        mock_embed.return_value = [[0.1], [0.2]]
        mock_replace.return_value = 2

        result = index_retailstar_docs(docs_dir=self.docs_dir, db=self.mock_db)

        self.assertEqual(result.chunk_count, 2)
        ingested_chunks = mock_embed.call_args.args[0]
        self.assertEqual(len(ingested_chunks), 2)
        self.assertEqual(ingested_chunks[0].metadata["title"], "Sample Policy")
        mock_replace.assert_called_once()
        replace_kwargs = {
            "embedding_model": mock_replace.call_args.args[3],
        }
        self.assertEqual(replace_kwargs["embedding_model"], settings.openai_embedding_model)


if __name__ == "__main__":
    unittest.main()
