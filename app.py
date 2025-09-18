"""Streamlit app that searches legal cases stored in MongoDB."""
from __future__ import annotations

import os
import textwrap
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from db import MongoCaseRepository, RepositoryError
from sample_data import SAMPLE_CASES


def _format_date(value: Optional[str]) -> str:
    """Return a human readable date string."""
    if not value:
        return "Unknown"
    try:
        return datetime.fromisoformat(value).strftime("%d %b %Y")
    except ValueError:
        return value


def _render_case(case: Dict[str, Any]) -> None:
    """Render a single case card."""
    title = case.get("case_title", "Untitled case")
    subtitle = f"{case.get('court', 'Unknown court')} · {_format_date(case.get('judgment_date'))}"

    with st.chat_message("assistant"):
        st.markdown(f"**{title}**  \\n{subtitle}")

        if citation := case.get("citation"):
            st.caption(citation)

        if summary := case.get("search_metadata", {}).get("summary"):
            st.write(summary)

        if issues := case.get("issues"):
            with st.expander("Key Issues", expanded=False):
                for issue in issues:
                    st.markdown(f"- {issue}")

        if reasoning := case.get("reasoning"):
            with st.expander("Reasoning", expanded=False):
                for key, value in reasoning.items():
                    title = key.replace("_", " ").title()
                    st.markdown(f"**{title}**\n\n{textwrap.fill(value, 100)}")

        if outcome := case.get("outcome"):
            with st.expander("Outcome", expanded=False):
                if decision := outcome.get("decision"):
                    st.markdown(f"**Decision**: {decision}")
                if directions := outcome.get("directions"):
                    st.markdown("**Directions**:")
                    for direction in directions:
                        st.markdown(f"- {direction}")

        if bench := case.get("bench"):
            st.caption("Bench: " + ", ".join(bench))


def _render_user_message(query: str) -> None:
    with st.chat_message("user"):
        st.write(query)


def _load_repository() -> MongoCaseRepository:
    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    database = os.environ.get("MONGODB_DB", "law")
    collection = os.environ.get("MONGODB_COLLECTION", "cases")
    return MongoCaseRepository(uri=mongo_uri, database=database, collection=collection)


def _search_cases(repository: MongoCaseRepository, query: str) -> List[Dict[str, Any]]:
    try:
        return repository.search_cases(query)
    except RepositoryError as exc:  # pragma: no cover - defensive programming
        st.error(str(exc))
        return []


def main() -> None:
    st.set_page_config(page_title="Legal Research Copilot", page_icon="⚖️", layout="wide")
    st.title("Legal Research Copilot")
    st.caption("Search Supreme Court judgments like you chat with GPT.")

    repository = _load_repository()

    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.chat_input("Ask about a case, citation, issue, or judge")

    if query:
        _render_user_message(query)
        results = _search_cases(repository, query)
        if not results:
            with st.chat_message("assistant"):
                st.write("No results from MongoDB. Showing sample cases instead.")
            for case in SAMPLE_CASES:
                _render_case(case)
        else:
            for case in results:
                _render_case(case)
        st.session_state.history.append({"query": query, "results": results})

    # Display history in sidebar
    with st.sidebar:
        st.header("Search configuration")
        st.write(
            "Configure MongoDB via environment variables: "
            "`MONGODB_URI`, `MONGODB_DB`, `MONGODB_COLLECTION`."
        )
        st.subheader("Recent queries")
        if history := st.session_state.get("history"):
            for entry in history[-5:][::-1]:
                st.markdown(f"- {entry['query']}")
        else:
            st.caption("Your latest searches will appear here.")


if __name__ == "__main__":
    main()
