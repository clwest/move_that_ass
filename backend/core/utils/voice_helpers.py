"""Helpers for working with voice journals using the OpenAI SDK."""

# NOTE: This file uses the OpenAI v1 SDK (client-based). Do not revert to old ChatCompletion or Audio.transcribe calls.

from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_audio(file_path: str) -> str:
    """Transcribe the given audio file using OpenAI Whisper."""

    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        return response.text


def summarize_text(text: str) -> str:
    """Summarize a piece of text using GPT-4."""

    prompt = (
        "Summarize the following voice journal in 2-3 sentences:\n\n" + text
    )

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

    return response.choices[0].message.content.strip()
