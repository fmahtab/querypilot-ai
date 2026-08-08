import unittest
from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.models.rag_chunk import RagChunk
from app.services.rag.retrieval import retrieve_retailstar_docs


class TestRetrieveRetailstarDocs(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_db = MagicMock()

    @patch("app.services.rag.retrieval.search_similar_chunks")
    @patch("app.services.rag.retrieval.embed_query")
    def test_orchestrates_embed_then_search(
        self,
        mock_embed_query: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        mock_embed_query.return_value = [0.1, 0.2, 0.3]
        mock_row = RagChunk(
            chunk_id="inventory_policy.md::chunk-002",
            source_file="inventory_policy.md",
            content="### Low inventory\n\nBelow minimum threshold.",
            embedding=[0.1, 0.2],
            embedding_model=settings.openai_embedding_model,
            chunk_metadata={
                "title": "Inventory Policy",
                "heading": "Low inventory",
                "source_file": "inventory_policy.md",
            },
        )
        mock_search.return_value = [(mock_row, 0.87)]
        call_order: list[str] = []

        mock_embed_query.side_effect = lambda question: call_order.append("embed") or [0.1, 0.2, 0.3]
        mock_search.side_effect = (
            lambda db, embedding, top_k, model: call_order.append("search") or [(mock_row, 0.87)]
        )

        result = retrieve_retailstar_docs("What is low inventory?", db=self.mock_db)

        self.assertEqual(call_order, ["embed", "search"])
        mock_embed_query.assert_called_once_with("What is low inventory?")
        mock_search.assert_called_once_with(
            self.mock_db,
            [0.1, 0.2, 0.3],
            settings.rag_top_k,
            settings.openai_embedding_model,
        )
        self.assertEqual(result.question, "What is low inventory?")
        self.assertEqual(result.top_k, settings.rag_top_k)
        self.assertEqual(len(result.chunks), 1)
        self.assertEqual(result.chunks[0].chunk_id, "inventory_policy.md::chunk-002")
        self.assertEqual(result.chunks[0].source_file, "inventory_policy.md")
        self.assertEqual(result.chunks[0].cosine_similarity, 0.87)
        self.assertEqual(result.chunks[0].metadata["heading"], "Low inventory")

    @patch("app.services.rag.retrieval.search_similar_chunks")
    @patch("app.services.rag.retrieval.embed_query")
    def test_uses_custom_top_k_when_provided(
        self,
        mock_embed_query: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        mock_embed_query.return_value = [0.1]
        mock_search.return_value = []

        result = retrieve_retailstar_docs("Returns policy?", top_k=3, db=self.mock_db)

        mock_search.assert_called_once_with(
            self.mock_db,
            [0.1],
            3,
            settings.openai_embedding_model,
        )
        self.assertEqual(result.top_k, 3)

    @patch("app.services.rag.retrieval.search_similar_chunks")
    @patch("app.services.rag.retrieval.embed_query")
    def test_strips_whitespace_from_question(
        self,
        mock_embed_query: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        mock_embed_query.return_value = [0.1]
        mock_search.return_value = []

        result = retrieve_retailstar_docs("  What is low inventory?  ", db=self.mock_db)

        mock_embed_query.assert_called_once_with("What is low inventory?")
        self.assertEqual(result.question, "What is low inventory?")

    def test_raises_for_empty_question(self) -> None:
        with self.assertRaises(ValueError):
            retrieve_retailstar_docs("   ", db=self.mock_db)

        with self.assertRaises(ValueError):
            retrieve_retailstar_docs("", db=self.mock_db)


if __name__ == "__main__":
    unittest.main()
