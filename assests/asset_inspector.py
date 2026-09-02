import os
import sys

def inspect_assets(directory: str = None) -> list:
    """Inspect image asset metadata and return detailed list."""
    if directory is None:
        directory = os.path.dirname(__file__)

    if not os.path.exists(directory):
        print(f"Error: Asset directory '{directory}' not found.")
        return []

    asset_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
    results = []

    try:
        from PIL import Image
        pil_available = True
    except ImportError:
        pil_available = False

    for fname in asset_files:
        fpath = os.path.join(directory, fname)
        size_bytes = os.path.getsize(fpath)

        width, height, img_format = None, None, "Unknown"
        if pil_available:
            try:
                with Image.open(fpath) as img:
                    width, height = img.size
                    img_format = img.format
            except Exception as e:
                img_format = f"Error ({e})"

        item = {
            "name": fname,
            "path": fpath,
            "size_bytes": size_bytes,
            "size_kb": round(size_bytes / 1024.0, 2),
            "width": width,
            "height": height,
            "format": img_format
        }
        results.append(item)

    return results

def print_report(assets: list):
    """Print Markdown formatted asset inspection summary."""
    print("\n# Asset Inspection Report")
    print(f"Total Assets Found: {len(assets)}\n")
    print("| Asset Name | Size (KB) | Dimensions (WxH) | Format | Status |")
    print("|---|---|---|---|---|")
    for item in assets:
        dim_str = f"{item['width']}x{item['height']}" if item['width'] else "N/A"
        status = "✅ Valid" if item['size_bytes'] > 0 else "❌ Empty File"
        print(f"| `{item['name']}` | {item['size_kb']} KB | {dim_str} | {item['format']} | {status} |")

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    assets = inspect_assets(target_dir)
    print_report(assets)

if __name__ == '__main__':
    main()
