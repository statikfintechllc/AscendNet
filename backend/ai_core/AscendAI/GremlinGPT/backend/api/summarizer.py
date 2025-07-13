# backend/api/summarizer.py  # type: ignore


def summarize_text(text):
    """Stub summarizer: returns the first 128 characters with ellipsis if too long."""
    if not isinstance(text, str):
        return ""
    return text[:128] + ("..." if len(text) > 128 else "")
