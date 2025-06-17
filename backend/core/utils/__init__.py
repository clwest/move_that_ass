# Shared utility helpers for the core app


def clean_text(text: str) -> str:
    """Sanitize text by removing common mis-encodings."""
    return (
        text.encode("utf-8", "ignore").decode("utf-8")
        .replace("â€™", "'")
        .replace("â€“", "-")
        .replace("â€œ", '"')
        .replace("â€", '"')
        .replace("â", "'")
        .replace("▒", "")
    )

