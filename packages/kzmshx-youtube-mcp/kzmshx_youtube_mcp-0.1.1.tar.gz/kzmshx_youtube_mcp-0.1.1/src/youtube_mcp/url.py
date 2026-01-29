"""YouTube URL parsing utilities."""

import re
from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> str:
    """Extract video ID from various forms of YouTube URLs.

    Handles standard, shortened, embed, shorts, live URLs,
    as well as regional domains and mobile versions.

    Args:
        url: YouTube URL or video ID

    Returns:
        The extracted video ID

    Raises:
        ValueError: If the video ID cannot be extracted
    """
    if not url:
        raise ValueError("URL is required")

    # Handle case where input is just the 11-character video ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url

    # Prepend scheme if not present
    if not re.match(r"https?://", url):
        url = "https://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        raise ValueError(f"Could not parse URL: {url}")

    # youtu.be shortlinks
    if hostname == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0].split("?")[0]
        if video_id:
            return video_id
        raise ValueError(f"Could not extract video ID from URL: {url}")

    # youtube.com variants
    youtube_pattern = r"^(?:www\.|m\.|music\.)?youtube\.com$"
    if not re.match(youtube_pattern, hostname):
        raise ValueError(f"Not a YouTube URL: {url}")

    # /watch?v=VIDEO_ID
    if parsed.path == "/watch":
        query_params = parse_qs(parsed.query)
        video_ids = query_params.get("v")
        if video_ids:
            return video_ids[0]
        raise ValueError(f"Could not extract video ID from URL: {url}")

    # /embed/VIDEO_ID, /shorts/VIDEO_ID, /live/VIDEO_ID, /v/VIDEO_ID
    path_parts = parsed.path.split("/")
    if len(path_parts) >= 3 and path_parts[1] in ("embed", "shorts", "live", "v"):
        video_id = path_parts[2].split("?")[0]
        if video_id:
            return video_id

    raise ValueError(f"Could not extract video ID from URL: {url}")
