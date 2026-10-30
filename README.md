# Adobe Motion Templates & Tools

A small open-source toolkit for organizing and documenting motion-design assets used with Adobe After Effects and Premiere Pro.

## Motion Asset Catalog

`motion_asset_catalog.py` scans a folder for common creative-production files and generates:

- `index.html`: a searchable, dark-themed HTML catalog.
- `assets.csv`: a spreadsheet-friendly inventory with file type, relative path, size, and modified date.

It uses only the Python standard library. No third-party packages are required.

### Requirements

- Python 3.9 or newer
- macOS, Windows, or Linux

### Run it

```bash
python motion_asset_catalog.py "/path/to/your/assets"
```

Choose an output folder:

```bash
python motion_asset_catalog.py "/path/to/your/assets" --output catalog
```

Scan only the selected folder, not subfolders:

```bash
python motion_asset_catalog.py "/path/to/your/assets" --top-level-only
```

Open `motion-asset-catalog/index.html` in a browser to search the catalog. Open `assets.csv` in Excel or Google Sheets.

### Supported file types

After Effects (`.aep`, `.aepx`, `.ffx`), Premiere Pro (`.prproj`, `.mogrt`), scripts (`.jsx`, `.jsxbin`), LUTs (`.cube`, `.look`), and common media/design files.

### Run tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs these tests automatically on pushes and pull requests.

## Project status

This is an early-stage project. Contributions, bug reports, and feature suggestions are welcome. Please open an issue before proposing large changes.

## License

MIT. See [LICENSE](LICENSE).
