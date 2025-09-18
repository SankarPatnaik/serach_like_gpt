# Legal Research Copilot

A Streamlit application that lets you search Supreme Court of India decisions stored in MongoDB using a conversational interface similar to ChatGPT.

## Features

- 💬 **Chat-style search** – ask questions in natural language using the Streamlit chat input.
- 🔎 **MongoDB powered** – retrieves matching cases via MongoDB text search (with a regex fallback when no text index exists).
- 🧠 **Semantic reranking** – reorders Mongo results by similarity using sentence-transformer embeddings.
- 📚 **Rich case cards** – displays summaries, issues, reasoning, and outcomes in expandable sections.
- 🆘 **Offline sample data** – shows curated sample results when MongoDB is unreachable so you can preview the UI immediately.

## Getting started

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set MongoDB connection details (defaults shown):

   ```bash
   export MONGODB_URI="mongodb://localhost:27017"
   export MONGODB_DB="law"
   export MONGODB_COLLECTION="cases"
   ```

4. Ensure your MongoDB collection has either a [text index](https://www.mongodb.com/docs/manual/core/index-text/) on key fields or contains documents similar to the sample schema provided in `sample_data.py`.

5. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

6. Open the URL shown in your terminal (usually <http://localhost:8501>) and start chatting with the legal research copilot.

## MongoDB schema expectations

The app assumes each MongoDB document follows the structure illustrated below:

```json
{
  "case_title": "In Re: … vs Director General (Prisons)",
  "court": "SUPREME COURT OF INDIA",
  "judgment_date": "2023-03-24",
  "citation": "2023 0 CJ(SC) 242",
  "bench": ["M.R. Shah", "C.T. Ravikumar"],
  "issues": ["Whether the non-disclosure …"],
  "reasoning": {
    "rejection_of_high_court_methodology": "…"
  },
  "outcome": {
    "decision": "The appeals were allowed …",
    "directions": ["Set aside …"]
  },
  "search_metadata": {
    "summary": "The Supreme Court allowed …"
  }
}
```

Additional keys are preserved and made available through expanders if desired.

## Configuration tips

- **Text search:** Create a text index covering `case_title`, `issues`, and `search_metadata.summary` to get the best ranking results.
- **Connection errors:** When the app cannot reach MongoDB it will show a helpful error message and fall back to the bundled sample case data.
- **Deployment:** Streamlit apps can be deployed on Streamlit Community Cloud, Hugging Face Spaces, or any environment that supports Python + MongoDB networking.

## Development

- Formatters/linters are not enforced, but keeping imports sorted and functions small makes maintenance easier.
- Run `python -m compileall .` to perform a quick syntax check before committing changes.

## License

This project is provided as-is for demonstration purposes.
