"""MongoDB repository helpers for the Streamlit app."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pymongo import MongoClient, errors


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

        try:
            cursor = collection.find(
                {"$text": {"$search": query}},
                {
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
                },
                sort=[("score", {"$meta": "textScore"})],
                limit=self.limit,
            )
        except errors.OperationFailure:
            cursor = collection.find(
                {
                    "$or": [
                        {"case_title": {"$regex": query, "$options": "i"}},
                        {"issues": {"$regex": query, "$options": "i"}},
                        {"search_metadata.summary": {"$regex": query, "$options": "i"}},
                    ]
                },
                limit=self.limit,
            )
        except errors.PyMongoError as exc:  # pragma: no cover - depends on runtime
            raise RepositoryError("Failed to run search query against MongoDB.") from exc

        documents: List[Dict[str, Any]] = []
        for document in cursor:
            documents.append(self._normalise_document(document))

        return documents

    def _normalise_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if document is None:
            return {}
        normalised = dict(document)
        identifier = normalised.get("_id")
        if identifier is not None:
            normalised["_id"] = str(identifier)
        normalised.pop("score", None)
        return normalised

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._collection = None
