import requests
import os

def download_file(url, save_path):
    if os.path.exists(save_path):
        print(f"ℹ️ Already downloaded: {save_path}")
        return save_path
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"✅ Downloaded: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return None
