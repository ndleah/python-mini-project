import os
import sys
import requests
from datetime import datetime

def fetch_nasa_apod(date_str: str = None, api_key: str = "DEMO_KEY") -> dict:
    """Fetch Astronomy Picture of the Day (APOD) from NASA API."""
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    if date_str:
        url += f"&date={date_str}"

    print(f"Fetching NASA APOD metadata from API...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"NASA API returned status code {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"Notice: Network request to NASA API failed ({e}). Using demo metadata fallback.")

    # Offline / Demo Fallback Metadata
    return {
        "title": "The Pillars of Creation (Hubble / James Webb Space Telescope)",
        "date": date_str or datetime.now().strftime("%Y-%m-%d"),
        "explanation": "The Pillars of Creation are elephant trunks of interstellar gas and dust in the Eagle Nebula, some 6,500–7,000 light-years from Earth.",
        "url": "https://images-assets.nasa.gov/image/PIA12345/PIA12345~orig.jpg",
        "media_type": "image"
    }

def download_and_save_image(apod_data: dict, output_dir: str = None) -> str:
    """Download APOD image and save to Astro_Images directory."""
    script_dir = os.path.dirname(__file__)
    if output_dir is None:
        output_dir = os.path.join(script_dir, "Astro_Images")

    os.makedirs(output_dir, exist_ok=True)
    title = apod_data.get("title", "NASA_APOD").replace(" ", "_").replace("/", "_")
    date_val = apod_data.get("date", "latest")
    image_url = apod_data.get("url", "")
    filename = f"{date_val}_{title[:30]}.jpg"
    file_path = os.path.join(output_dir, filename)

    print(f"\n--- NASA Astronomy Picture of the Day ---")
    print(f"Title      : {apod_data.get('title')}")
    print(f"Date       : {apod_data.get('date')}")
    print(f"Explanation: {apod_data.get('explanation')}\n")

    if image_url.startswith("http"):
        try:
            img_res = requests.get(image_url, timeout=15)
            if img_res.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(img_res.content)
                print(f"Image successfully downloaded and saved to: {file_path}")
                return file_path
        except Exception as e:
            print(f"Could not download image from URL ({e}).")

    # Create dummy placeholder file if offline download failed
    with open(file_path, "w") as f:
        f.write(f"NASA APOD Metadata:\nTitle: {apod_data.get('title')}\nExplanation: {apod_data.get('explanation')}\n")
    print(f"Metadata summary saved to: {file_path}")
    return file_path

def main():
    date_param = sys.argv[1] if len(sys.argv) > 1 else None
    data = fetch_nasa_apod(date_str=date_param)
    download_and_save_image(data)

if __name__ == '__main__':
    main()
