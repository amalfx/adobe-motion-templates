#!/usr/bin/env python3
"""Build a searchable HTML and CSV inventory of Adobe motion-design assets."""

from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path
from datetime import datetime
from typing import Iterable

SUPPORTED_EXTENSIONS = {
    ".aep", ".aepx", ".mogrt", ".prproj", ".ffx", ".jsx", ".jsxbin",
    ".cube", ".look", ".png", ".jpg", ".jpeg", ".svg", ".wav", ".mp3",
    ".mp4", ".mov", ".webm", ".psd", ".ai", ".pdf"
}


def collect_assets(folder: Path, recursive: bool = True) -> list[dict[str, str | int]]:
    """Return metadata for supported files under folder."""
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder does not exist or is not a directory: {folder}")

    paths: Iterable[Path] = folder.rglob("*") if recursive else folder.glob("*")
    assets = []
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        stat = path.stat()
        assets.append({
            "name": path.name,
            "type": path.suffix.lower().lstrip(".").upper(),
            "relative_path": str(path.relative_to(folder)),
            "size_bytes": stat.st_size,
            "size": format_size(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime).astimezone().strftime("%Y-%m-%d %H:%M"),
        })
    return sorted(assets, key=lambda item: str(item["relative_path"]).lower())


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024
    return f"{value:.1f} GB"


def write_csv(assets: list[dict[str, str | int]], destination: Path) -> None:
    fields = ["name", "type", "relative_path", "size_bytes", "size", "modified"]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(assets)


def write_html(assets: list[dict[str, str | int]], destination: Path, source: Path) -> None:
    rows = []
    for asset in assets:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(asset['name']))}</td>"
            f"<td><span class=\"tag\">{html.escape(str(asset['type']))}</span></td>"
            f"<td>{html.escape(str(asset['relative_path']))}</td>"
            f"<td>{html.escape(str(asset['size']))}</td>"
            f"<td>{html.escape(str(asset['modified']))}</td>"
            "</tr>"
        )
    body = "\n".join(rows) or '<tr><td colspan="5">No supported assets found.</td></tr>'
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Motion Asset Catalog</title>
<style>
:root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; }}
body {{ margin: 0; padding: 32px; background: #10131a; color: #edf1f7; }}
main {{ max-width: 1100px; margin: auto; }}
h1 {{ margin-bottom: 6px; }}
.sub {{ color: #aab4c4; margin-top: 0; }}
input {{ width: min(100%, 460px); padding: 12px 14px; margin: 18px 0; border: 1px solid #384253; border-radius: 9px; background: #191f2a; color: white; }}
table {{ width: 100%; border-collapse: collapse; background: #171d27; border-radius: 12px; overflow: hidden; }}
th, td {{ padding: 12px 14px; border-bottom: 1px solid #2a3341; text-align: left; font-size: 14px; }}
th {{ color: #b8c5d8; background: #202938; position: sticky; top: 0; }}
tr:hover td {{ background: #202938; }}
.tag {{ background: #293b55; color: #c9e0ff; border-radius: 5px; padding: 3px 7px; }}
.count {{ color: #aab4c4; font-size: 14px; }}
</style>
</head>
<body><main>
<h1>🎬 Motion Asset Catalog</h1>
<p class="sub">Inventory for: {html.escape(str(source.resolve()))}</p>
<p class="count">{len(assets)} supported asset(s) indexed</p>
<input id="filter" type="search" placeholder="Search by filename, type, or folder…" aria-label="Filter assets">
<table><thead><tr><th>File</th><th>Type</th><th>Folder / Path</th><th>Size</th><th>Modified</th></tr></thead>
<tbody id="assets">{body}</tbody></table>
</main>
<script>
const filter = document.getElementById('filter');
filter.addEventListener('input', () => {{
  const query = filter.value.toLowerCase();
  document.querySelectorAll('#assets tr').forEach(row => {{
    row.hidden = !row.textContent.toLowerCase().includes(query);
  }});
}});
</script>
</body></html>"""
    destination.write_text(page, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a searchable HTML and CSV catalog of Adobe motion assets."
    )
    parser.add_argument("folder", type=Path, help="Folder containing your assets")
    parser.add_argument("-o", "--output", type=Path, default=Path("motion-asset-catalog"),
                        help="Output directory (default: ./motion-asset-catalog)")
    parser.add_argument("--top-level-only", action="store_true",
                        help="Do not scan subfolders")
    args = parser.parse_args()

    try:
        assets = collect_assets(args.folder.expanduser(), recursive=not args.top_level_only)
        args.output.mkdir(parents=True, exist_ok=True)
        csv_path = args.output / "assets.csv"
        html_path = args.output / "index.html"
        write_csv(assets, csv_path)
        write_html(assets, html_path, args.folder.expanduser())
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Indexed {len(assets)} asset(s).")
    print(f"HTML catalog: {html_path.resolve()}")
    print(f"CSV inventory: {csv_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
