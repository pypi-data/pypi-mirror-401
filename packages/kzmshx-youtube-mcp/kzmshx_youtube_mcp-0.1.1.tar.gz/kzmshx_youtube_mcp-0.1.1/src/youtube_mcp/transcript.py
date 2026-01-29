"""Transcript extraction using youtube-transcript-api."""

from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from youtube_mcp.url import extract_video_id


def format_timestamp(seconds: float) -> str:
    """Format seconds as [H:MM:SS] or [M:SS]."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"[{hours}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes}:{secs:02d}]"


def get_transcript(
    url: str,
    language: str = "auto",
    with_timestamps: bool = False,
) -> dict[str, Any]:
    """Get transcript text from a YouTube video.

    Args:
        url: YouTube URL or video ID
        language: Language code (default: auto-detect)
        with_timestamps: Include timestamps in output

    Returns:
        Dict containing video_id, language, and transcript text
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    # Get available transcripts
    transcript_list = api.list(video_id)

    # Determine language priority (English first, then Japanese for auto; otherwise specified + English)
    preferred_languages = ["en", "ja"] if language == "auto" else [language, "en"]

    # Find transcript
    transcript = None
    used_language = None

    # Try manual transcripts first
    for lang in preferred_languages:
        try:
            transcript = transcript_list.find_transcript([lang])
            used_language = lang
            break
        except NoTranscriptFound:
            continue

    # Fall back to any available transcript
    if transcript is None:
        for t in transcript_list:
            transcript = t
            used_language = t.language_code
            break

    if transcript is None:
        return {
            "video_id": video_id,
            "language": None,
            "transcript": None,
            "error": "No transcript found",
        }

    # Fetch and format transcript
    entries = transcript.fetch()

    if with_timestamps:
        lines = [f"{format_timestamp(entry.start)} {entry.text}" for entry in entries]
    else:
        lines = [entry.text for entry in entries]

    return {
        "video_id": video_id,
        "language": used_language,
        "transcript": "\n".join(lines),
    }
