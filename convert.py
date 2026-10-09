#!/usr/bin/env python3
"""Converte una playlist M3U/M3U8 in una lista JSON compatibile con lo schema di Zappr."""
import argparse
import json
import re
import sys
import urllib.request

LOGO_SUFFIX = "?raw=1"  # lo schema vieta URL di logo che finiscono con .png/.webp
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def read_source(src):
    if re.match(r"^https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "m3u-to-zappr/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8-sig", errors="replace")
    with open(src, encoding="utf-8-sig") as f:
        return f.read()


def parse_m3u(text):
    """Restituisce una lista di dict {attrs, name, url}."""
    entries, current = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            body = line[len("#EXTINF:"):]
            attrs = {m.group(1).lower(): m.group(2) for m in ATTR_RE.finditer(body)}
            last_end = max((m.end() for m in ATTR_RE.finditer(body)), default=0)
            rest = body[last_end:]
            if last_end == 0 or "," not in rest:
                rest = body
            name = rest.split(",", 1)[1].strip() if "," in rest else ""
            current = {"attrs": attrs, "name": name or attrs.get("tvg-name", "")}
        elif line.startswith("#"):
            continue
        elif current is not None:
            current["url"] = line
            entries.append(current)
            current = None
    return entries


def detect_stream(url):
    """Ritorna (type, url) secondo i tipi supportati dallo schema Zappr."""
    m = re.search(r"(?:youtube\.com/watch\?(?:.*&)?v=|youtu\.be/|youtube\.com/live/)([\w-]+)", url)
    if m:
        return "youtube", m.group(1)
    m = re.search(r"youtube\.com/channel/([\w-]+)", url)
    if m:
        return "youtube", m.group(1)
    m = re.match(r"https?://(?:www\.)?twitch\.tv/(\w+)/?$", url)
    if m:
        return "twitch", m.group(1)
    path = url.split("?")[0].lower()
    if path.endswith(".mpd"):
        return "dash", url
    if path.endswith((".m3u8", ".m3u")):
        return "hls", url
    if path.endswith((".mp3", ".aac", ".ogg")):
        return "audio", url
    if path.endswith((".mp4", ".webm")):
        return "direct", url
    return "hls", url  # default, segnalato nei warning


def build_channels(entries, warnings):
    channels = []
    used = set()
    for e in entries:
        try:
            used.add(int(float(e["attrs"]["tvg-chno"])))
        except (KeyError, ValueError):
            pass
    auto_lcn = max(used, default=0)
    for e in entries:
        a, name, url = e["attrs"], e["name"], e["url"]

        try:
            lcn = int(float(a["tvg-chno"]))
        except (KeyError, ValueError):
            auto_lcn += 1
            lcn = auto_lcn
            warnings.append(f"'{name}': tvg-chno mancante, assegnato LCN {lcn}")

        logo = a.get("tvg-logo", "")
        if not logo:
            warnings.append(f"'{name}': logo mancante (campo obbligatorio dello schema)")
        elif re.search(r"\.(png|webp)$", logo, re.I):
            logo += LOGO_SUFFIX

        ch = {"lcn": lcn, "logo": logo}

        if name.upper().endswith(" HD"):
            name = name[:-3].rstrip()
            ch["hd"] = True
        ch["name"] = name
        if re.search(r"\b(4K|UHD)$", name, re.I):
            ch["uhd"] = True

        stype, surl = detect_stream(url)
        known = re.search(r"\.(mpd|m3u8?|mp3|aac|ogg|mp4|webm)(\?|$)", url, re.I) or stype in ("youtube", "twitch")
        if not known:
            warnings.append(f"'{name}': tipo stream non riconosciuto, assunto 'hls' ({url})")
        ch["type"], ch["url"] = stype, surl
        if url.lower().startswith("http://"):
            ch["http"] = True

        channels.append(ch)
    return channels


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", help="URL o percorso della playlist M3U")
    p.add_argument("-o", "--output", default="channels.json")
    p.add_argument("--name", default="Lista convertita")
    p.add_argument("--publisher", default="Sconosciuto")
    p.add_argument("--publisher-link", default="")
    p.add_argument("--epg", default="", help="URL EPG (default: disattivato). Deve avere CORS abilitato.")
    args = p.parse_args()

    warnings = []
    entries = parse_m3u(read_source(args.source))
    if not entries:
        sys.exit("Nessun canale trovato: il file è davvero una playlist M3U?")

    out = {"name": args.name, "publisher": args.publisher}
    if args.publisher_link:
        out["publisherLink"] = args.publisher_link
    out["epg"] = args.epg if args.epg else False
    out["channels"] = build_channels(entries, warnings)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=4)
        f.write("\n")

    print(f"Convertiti {len(out['channels'])} canali -> {args.output}")
    for w in warnings:
        print(f"::warning::{w}")


if __name__ == "__main__":
    main()
