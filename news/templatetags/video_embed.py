# -*- coding: utf-8 -*-
"""Template filters for embedding video URLs.
Converts regular YouTube or Vimeo URLs into embed URLs suitable for <iframe>.
"""

import re
from urllib.parse import urlparse, parse_qs

from django import template

register = template.Library()

YOUTUBE_WATCH_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)")
YOUTUBE_SHORT_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtu\.be/([^?&]+)")
YOUTUBE_SHORTS_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([^?&]+)")
YOUTUBE_LIVE_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/live/([^?&]+)")
VIMEO_REGEX = re.compile(r"(?:https?://)?(?:www\.)?vimeo\.com/(\d+)")

@register.filter(name='embed_url')
def embed_url(url):
    """Return an embed-friendly URL for YouTube or Vimeo.
    If the URL is already an embed URL, it is returned unchanged.
    """
    if not url:
        return ''
    # YouTube long URL
    m = YOUTUBE_WATCH_REGEX.search(url)
    if m:
        video_id = m.group(1)
        embed = f"https://www.youtube.com/embed/{video_id}"
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'list' in qs:
            embed += f"?list={qs['list'][0]}"
        return embed
    # YouTube short URL
    m = YOUTUBE_SHORT_REGEX.search(url)
    if m:
        video_id = m.group(1)
        embed = f"https://www.youtube.com/embed/{video_id}"
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'list' in qs:
            embed += f"?list={qs['list'][0]}"
        return embed
    # YouTube Shorts
    m = YOUTUBE_SHORTS_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    # YouTube Live
    m = YOUTUBE_LIVE_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    # Vimeo URL
    m = VIMEO_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"https://player.vimeo.com/video/{video_id}"
    # If already an embed URL or unknown format, return as‑is
    return url
