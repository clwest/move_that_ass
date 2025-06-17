"""Helpers for working with voice journals using the OpenAI SDK."""

# NOTE: This file uses the OpenAI v1 SDK (client-based). Do not revert to old ChatCompletion or Audio.transcribe calls.

from openai import OpenAI
from dotenv import load_dotenv
import os

from . import clean_text
load_dotenv()

try:
    client = OpenAI()
except Exception:
    client = None




def transcribe_audio(file_path: str) -> str:
    """Transcribe the given audio file using OpenAI Whisper."""
    if client is None:
        return ""
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        return clean_text(response.text)


def summarize_text(text: str) -> str:
    """Summarize a piece of text using GPT-4."""

    prompt = (
        "Summarize the following voice journal in 2-3 sentences:\n\n" + text
    )

    if client is None:
        return prompt
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": "You're a helpful assistant who reflects on human thoughts.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return clean_text(response.choices[0].message.content.strip())


def generate_tags_from_text(text: str):
    """Generate 2-4 short tags summarizing a journal entry."""

    prompt = (
        "Analyze the following voice journal transcript and return a list of 2-4 "
        "lowercase tags that describe the tone or intent. Keep it JSON-safe and "
        "short.\n\nTranscript:\n" + text
    )

    if client is None:
        raw = "uncategorized"
    else:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You're a smart assistant that labels journal entries with short tags.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )


    raw = clean_text(response.choices[0].message.content.strip())


    try:
        tags = eval(raw) if raw.startswith("[") else [raw]
        return tags
    except Exception:
        return ["uncategorized"]
