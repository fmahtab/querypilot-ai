import unittest
from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.schemas.rag import DocumentChunk
from app.services.rag.embedding import build_embed_text, embed_chunks, embed_query


class TestBuildEmbedText(unittest.TestCase):
    def test_includes_document_title_section_path_and_content(self) -> None:
        chunk = DocumentChunk(
            chunk_id="sample.md::chunk-001",
            content="### Low inventory\n\nA SKU is flagged as low inventory.",
            metadata={
                "title": "RetailStar Inventory Policy",
                "section_path": ["RetailStar — Inventory Policy", "Stock Levels", "Low inventory"],
            },
        )

        embed_text = build_embed_text(chunk)

        self.assertIn("Document: RetailStar Inventory Policy", embed_text)
        self.assertIn(
            "Section: RetailStar — Inventory Policy > Stock Levels > Low inventory",
            embed_text,
        )
        self.assertIn("### Low inventory", embed_text)
        self.assertIn("A SKU is flagged as low inventory.", embed_text)

    def test_omits_section_line_when_section_path_empty(self) -> None:
        chunk = DocumentChunk(
            chunk_id="sample.md::chunk-000",
            content="# Title\n\nBody text.",
            metadata={"title": "Sample Doc", "section_path": []},
        )

        embed_text = build_embed_text(chunk)

        self.assertIn("Document: Sample Doc", embed_text)
        self.assertNotIn("Section:", embed_text)
        self.assertIn("# Title", embed_text)


class TestEmbedChunks(unittest.TestCase):
    def test_returns_empty_list_for_no_chunks(self) -> None:
        self.assertEqual(embed_chunks([]), [])

    @patch("app.services.rag.embedding.OpenAI")
    def test_calls_openai_with_enriched_texts(self, mock_openai_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.embeddings.create.return_value = MagicMock(
            data=[
                MagicMock(embedding=[0.1, 0.2, 0.3]),
                MagicMock(embedding=[0.4, 0.5, 0.6]),
            ]
        )

        chunks = [
            DocumentChunk(
                chunk_id="a.md::chunk-000",
                content="# A",
                metadata={"title": "Doc A", "section_path": ["A"]},
            ),
            DocumentChunk(
                chunk_id="b.md::chunk-001",
                content="# B",
                metadata={"title": "Doc B", "section_path": ["B"]},
            ),
        ]

        embeddings = embed_chunks(chunks, client=mock_client)

        mock_client.embeddings.create.assert_called_once()
        call_kwargs = mock_client.embeddings.create.call_args.kwargs
        self.assertEqual(call_kwargs["model"], settings.openai_embedding_model)
        self.assertEqual(call_kwargs["dimensions"], settings.embedding_dimensions)
        self.assertEqual(len(call_kwargs["input"]), 2)
        self.assertIn("Document: Doc A", call_kwargs["input"][0])
        self.assertIn("Document: Doc B", call_kwargs["input"][1])
        self.assertEqual(embeddings, [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])


class TestEmbedQuery(unittest.TestCase):
    @patch("app.services.rag.embedding.OpenAI")
    def test_embeds_raw_question_text(self, mock_openai_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
        )

        embedding = embed_query("What is low inventory?", client=mock_client)

        mock_client.embeddings.create.assert_called_once_with(
            model=settings.openai_embedding_model,
            input="What is low inventory?",
            dimensions=settings.embedding_dimensions,
        )
        self.assertEqual(embedding, [0.1, 0.2, 0.3])


if __name__ == "__main__":
    unittest.main()
