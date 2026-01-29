"""Tests for URL parsing."""

import pytest

from youtube_mcp.url import extract_video_id


class TestExtractVideoId:
    """Tests for extract_video_id function."""

    @pytest.mark.parametrize(
        "url,expected",
        [
            # Standard watch URL
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # With playlist
            (
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=WL&index=1",
                "dQw4w9WgXcQ",
            ),
            # Just the ID
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Shortened URL
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Shortened with tracking
            ("https://youtu.be/dQw4w9WgXcQ?si=abcde12345", "dQw4w9WgXcQ"),
            # Embed URL
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Mobile URL
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Music URL
            ("https://music.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # No scheme
            ("youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Old embed format
            ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            # Shorts
            ("https://www.youtube.com/shorts/o-YBDTqX_ZU", "o-YBDTqX_ZU"),
            # Live
            ("https://www.youtube.com/live/some_live_id", "some_live_id"),
        ],
    )
    def test_valid_urls(self, url: str, expected: str) -> None:
        """Test that valid URLs are parsed correctly."""
        assert extract_video_id(url) == expected

    @pytest.mark.parametrize(
        "url",
        [
            "",
            "https://www.google.com",
            "not a url",
            "https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw",
        ],
    )
    def test_invalid_urls(self, url: str) -> None:
        """Test that invalid URLs raise ValueError."""
        with pytest.raises(ValueError):
            extract_video_id(url)
