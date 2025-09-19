"""MongoDB repository helpers for the Streamlit app."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional, Set

from pymongo import MongoClient, errors
from sentence_transformers import SentenceTransformer


class RepositoryError(RuntimeError):
    """Raised when the Mongo repository cannot be accessed."""


@dataclass
class MongoCaseRepository:
    """Repository that wraps MongoDB access for legal case documents."""

    uri: str
    database: str
    collection: str
    limit: int = 5

    _client: Optional[MongoClient] = None
    _collection = None

    def _connect(self) -> None:
        if self._client is not None:
            return

        try:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
            # Trigger server selection to fail fast when the DB is unavailable.
            self._client.admin.command("ping")
            self._collection = self._client[self.database][self.collection]
        except errors.PyMongoError as exc:  # pragma: no cover - depends on runtime
            raise RepositoryError(
                "Could not connect to MongoDB. Please check your connection details."
            ) from exc

    @property
    def collection_handle(self):
        if self._collection is None:
            self._connect()
        return self._collection

    def search_cases(self, query: str) -> List[Dict[str, Any]]:
        """Search cases in MongoDB using a text index or regex fallback."""
        if not query:
            return []

        collection = self.collection_handle

        text_projection = {
            "score": {"$meta": "textScore"},
            "case_title": 1,
            "court": 1,
            "judgment_date": 1,
            "citation": 1,
            "bench": 1,
            "issues": 1,
            "reasoning": 1,
            "outcome": 1,
            "search_metadata": 1,
        }

        documents: List[Dict[str, Any]] = []
        run_fallback = False

        try:
            cursor = collection.find(
                {"$text": {"$search": query}},
                text_projection,
                sort=[("score", {"$meta": "textScore"})],
                limit=self.limit,
            )
            documents = [
                self._normalise_document(document)
                for document in cursor
            ]
        except errors.OperationFailure:
            run_fallback = True
        except errors.PyMongoError as exc:  # pragma: no cover - depends on runtime
            raise RepositoryError("Failed to run search query against MongoDB.") from exc

        if run_fallback or len(documents) < self.limit:
            fallback_documents = self._fallback_search(collection, query, text_projection)
            documents = self._merge_documents(documents, fallback_documents)

        reranked = self._semantic_rerank(query, documents)
        return reranked[: self.limit]

    def _fallback_search(
        self,
        collection,
        query: str,
        projection: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        fallback_projection = dict(projection)
        fallback_projection.pop("score", None)

        regex_filter = {
            "$or": [
                {"case_title": {"$regex": query, "$options": "i"}},
                {"issues": {"$regex": query, "$options": "i"}},
                {"search_metadata.summary": {"$regex": query, "$options": "i"}},
                {"court": {"$regex": query, "$options": "i"}},
                {"bench": {"$regex": query, "$options": "i"}},
                {"citation": {"$regex": query, "$options": "i"}},
            ]
        }

        cursor = collection.find(regex_filter, fallback_projection, limit=self.limit)
        return [self._normalise_document(document) for document in cursor]

    def _merge_documents(
        self,
        primary: List[Dict[str, Any]],
        secondary: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        if not secondary:
            return primary

        merged = list(primary)
        seen: Set[str] = {
            document["_id"]
            for document in primary
            if isinstance(document.get("_id"), str)
        }

        for document in secondary:
            identifier = document.get("_id")
            if isinstance(identifier, str):
                if identifier in seen:
                    continue
                seen.add(identifier)
            elif document in merged:
                continue
            merged.append(document)

        return merged

    def _normalise_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if document is None:
            return {}
        normalised = dict(document)
        identifier = normalised.get("_id")
        if identifier is not None:
            normalised["_id"] = str(identifier)
        normalised.pop("score", None)
        return normalised

    def _semantic_rerank(
        self, query: str, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        if len(documents) <= 1:
            return documents

        try:
            model = _get_embedding_model()
            doc_texts = [self._document_to_text(document) for document in documents]
            query_vector = model.encode(
                query, convert_to_numpy=True, normalize_embeddings=True
            )
            document_vectors = model.encode(
                doc_texts, convert_to_numpy=True, normalize_embeddings=True
            )
        except Exception:  # pragma: no cover - fallback when embeddings fail
            return documents

        scores = document_vectors @ query_vector
        ranked = sorted(
            zip(scores.tolist(), documents),
            key=lambda item: item[0],
            reverse=True,
        )
        return [document for _, document in ranked]

    def _document_to_text(self, document: Dict[str, Any]) -> str:
        parts: List[str] = []
        for key in ("case_title", "court", "citation"):
            value = document.get(key)
            if value:
                parts.append(str(value))

        bench = document.get("bench")
        if isinstance(bench, list):
            parts.extend(str(member) for member in bench if member)

        issues = document.get("issues")
        if isinstance(issues, list):
            parts.extend(str(issue) for issue in issues if issue)

        summary = document.get("search_metadata", {}).get("summary")
        if summary:
            parts.append(str(summary))

        reasoning = document.get("reasoning")
        if isinstance(reasoning, dict):
            parts.extend(str(text) for text in reasoning.values() if text)

        outcome = document.get("outcome")
        if isinstance(outcome, dict):
            decision = outcome.get("decision")
            if decision:
                parts.append(str(decision))
            directions = outcome.get("directions")
            if isinstance(directions, list):
                parts.extend(str(direction) for direction in directions if direction)

        return " ".join(parts)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._collection = None


@lru_cache(maxsize=1)
def _get_embedding_model() -> SentenceTransformer:
    """Return a cached embedding model for semantic similarity."""
    return SentenceTransformer("all-MiniLM-L6-v2")
