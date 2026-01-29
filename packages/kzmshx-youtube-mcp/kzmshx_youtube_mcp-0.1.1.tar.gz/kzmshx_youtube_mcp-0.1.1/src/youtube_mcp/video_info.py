"""Video metadata extraction using yt-dlp."""

from typing import Any

import yt_dlp

from youtube_mcp.url import extract_video_id


def get_video_info(url: str) -> dict[str, Any]:
    """Get metadata from a YouTube video.

    Args:
        url: YouTube URL or video ID

    Returns:
        Dict containing video metadata
    """
    video_id = extract_video_id(url)
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            if info is None:
                return {
                    "id": video_id,
                    "error": "Failed to extract video info",
                }

            # Collect available subtitle languages
            subtitles = info.get("subtitles", {})
            automatic_captions = info.get("automatic_captions", {})
            available_languages = sorted(set(subtitles.keys()) | set(automatic_captions.keys()))

            return {
                "id": video_id,
                "title": info.get("title"),
                "description": info.get("description"),
                "duration": info.get("duration"),
                "channel": info.get("channel") or info.get("uploader"),
                "upload_date": _format_date(info.get("upload_date")),
                "view_count": info.get("view_count"),
                "available_languages": available_languages,
            }

    except Exception as e:
        return {
            "id": video_id,
            "error": str(e),
        }


def _format_date(date_str: str | None) -> str | None:
    """Format YYYYMMDD to YYYY-MM-DD."""
    if not date_str or len(date_str) != 8:
        return date_str
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
