# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse, parse_qs
from django import template

register = template.Library()

YOUTUBE_WATCH_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)")
YOUTUBE_SHORT_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtu\.be/([^?&]+)")
YOUTUBE_SHORTS_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([^?&]+)")
YOUTUBE_LIVE_REGEX = re.compile(r"(?:https?://)?(?:www\.)?youtube\.com/live/([^?&]+)")
VIMEO_REGEX = re.compile(r"(?:https?://)?(?:www\.)?vimeo\.com/(\d+)")

# Используем защищённый домен
YOUTUBE_EMBED = "https://www.youtube-nocookie.com/embed/"
VIMEO_EMBED = "https://player.vimeo.com/video/"

@register.filter(name='embed_url')
def embed_url(url):
    if not url:
        return ''

    # YouTube long URL
    m = YOUTUBE_WATCH_REGEX.search(url)
    if m:
        video_id = m.group(1)
        embed = f"{YOUTUBE_EMBED}{video_id}"
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'list' in qs:
            embed += f"?list={qs['list'][0]}"
        return embed

    # YouTube short URL
    m = YOUTUBE_SHORT_REGEX.search(url)
    if m:
        video_id = m.group(1)
        embed = f"{YOUTUBE_EMBED}{video_id}"
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'list' in qs:
            embed += f"?list={qs['list'][0]}"
        return embed

    # YouTube Shorts
    m = YOUTUBE_SHORTS_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"{YOUTUBE_EMBED}{video_id}"

    # YouTube Live
    m = YOUTUBE_LIVE_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"{YOUTUBE_EMBED}{video_id}"

    # Vimeo
    m = VIMEO_REGEX.search(url)
    if m:
        video_id = m.group(1)
        return f"{VIMEO_EMBED}{video_id}"

    return url
