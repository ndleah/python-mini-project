import os
import sys

def audit_image_assets(directory: str = None) -> list:
    """Scan and list image assets with file sizes, dimensions, and formats."""
    if directory is None:
        directory = os.path.dirname(__file__)

    valid_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg')
    assets = []

    try:
        from PIL import Image
        pil_available = True
    except ImportError:
        pil_available = False

    for fname in sorted(os.listdir(directory)):
        if fname.lower().endswith(valid_exts):
            fpath = os.path.join(directory, fname)
            size_kb = os.path.getsize(fpath) / 1024.0
            dimensions = "N/A"
            fmt = fname.split('.')[-1].upper()

            if pil_available and fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                try:
                    with Image.open(fpath) as img:
                        dimensions = f"{img.width}x{img.height}"
                        fmt = img.format or fmt
                except Exception:
                    pass

            assets.append({
                "filename": fname,
                "size_kb": round(size_kb, 1),
                "dimensions": dimensions,
                "format": fmt
            })

    return assets

def print_audit_report(assets: list):
    """Print markdown report of image documentation assets."""
    print("=== Documentation Image Assets Audit Report ===")
    print(f"{'Filename':<42} | {'Format':<8} | {'Size (KB)':<10} | {'Dimensions':<12}")
    print("-" * 80)
    total_size = 0.0
    for item in assets:
        total_size += item['size_kb']
        print(f"{item['filename']:<42} | {item['format']:<8} | {item['size_kb']:<10.1f} | {item['dimensions']:<12}")
    print("-" * 80)
    print(f"Total Assets: {len(assets)} | Total Size: {total_size / 1024.0:.2f} MB\n")

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    assets = audit_image_assets(target_dir)
    print_audit_report(assets)

if __name__ == '__main__':
    main()
