"""
embedding_service.py
---------------------
An "embedding" turns a piece of text into a list of numbers (a vector)
that represents its MEANING. Text with similar meaning ends up with
similar numbers, even if the words are totally different.

Example: "revenue increased" and "sales went up" would produce vectors
that are close together, even though they share almost no words.

We use a small, fast, free model from the sentence-transformers library
that runs entirely on your own machine (no API key needed).
"""

from sentence_transformers import SentenceTransformer

# Loading the model takes a few seconds, so we do it ONCE when this file
# is first imported, not every time we need an embedding.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> list[float]:
    """Turns a single string into a 384-number vector."""
    vector = _model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Same as above, but faster for many strings at once (batching)."""
    vectors = _model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]
