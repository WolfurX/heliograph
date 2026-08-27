"""RSS feed of findings. Subscribe and the anomalies come to you;
the page becomes something you never have to remember to open."""

from datetime import datetime, timezone
from xml.sax.saxutils import escape

SITE = "https://wolfurx.github.io/heliograph/"


def build(recent, generated_ts):
    """recent: [(ts, metric, severity, headline, detail), ...] newest first."""
    items = []
    for ts, metric, severity, headline, detail in recent:
        when = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        items.append(
            "<item>"
            f"<title>[{escape(severity.upper())}] {escape(headline)}</title>"
            f"<link>{SITE}</link>"
            f"<guid isPermaLink=\"false\">{ts}-{escape(metric)}</guid>"
            f"<pubDate>{when}</pubDate>"
            f"<description>{escape(detail)}</description>"
            "</item>"
        )
    now = datetime.fromtimestamp(generated_ts, tz=timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>'
        "<title>Heliograph findings</title>"
        f"<link>{SITE}</link>"
        "<description>Solana anomalies, pushed. Quiet means quiet.</description>"
        f"<lastBuildDate>{now}</lastBuildDate>"
        + "".join(items) +
        "</channel></rss>\n"
    )
