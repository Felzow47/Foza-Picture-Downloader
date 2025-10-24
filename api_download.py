import requests
import json
import os
import hashlib
from urllib.parse import urljoin

# Configuration
API_BASE_URL = "https://api.forza.net"
import json
import os
TOKEN_PATH = "forza_token.json"
if not os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump({"access_token": ""}, f)
with open(TOKEN_PATH, "r", encoding="utf-8") as f:
    ACCESS_TOKEN = json.load(f)["access_token"]
GAME = "FH5"  # or "FM", "FH4", "FM7"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


# Directory to save images
os.makedirs("Downloads", exist_ok=True)

# Log file for downloaded images
LOG_FILE = "downloaded_images.log"

def get_unique_filename(photo, index):
    # Use title, photo id, and hash of CDN path for uniqueness
    title = photo.get('title', f'photo_{index+1}').replace('/', '_').replace('\\', '_')
    photo_id = photo.get('id') or photo.get('photoId') or ''
    cdn_path = photo.get('photoCdnPath', '')
    hash_part = hashlib.md5(cdn_path.encode()).hexdigest()[:8]
    filename = f"{title}_{photo_id}_{hash_part}.jpg"
    return filename

def get_photos(game, continuation_token=None):
    url = f"{API_BASE_URL}/api/v4/me/gallery/{game}"
    if continuation_token:
        url += f"?continuationToken={continuation_token}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def is_already_downloaded(filename):
    if not os.path.exists(LOG_FILE):
        print(f"[LOG] No log file found, treating as first run.")
        return False
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        downloaded = f.read().splitlines()
        if filename in downloaded:
            print(f"[SKIP] Already in log: {filename}")
            return True
        else:
            print(f"[CHECK] Not in log: {filename}")
            return False

def log_download(filename):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(filename + '\n')
    print(f"[LOG] Added to log: {filename}")

def download_image(url, filename):
    print(f"[START] Checking: {filename}")
    if is_already_downloaded(filename):
        print(f"[SKIP] Already downloaded: {filename}")
        return
    try:
        print(f"[DOWNLOAD] Downloading from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join("Downloads", filename), 'wb') as f:
            f.write(response.content)
        log_download(filename)
        print(f"[SUCCESS] Downloaded: {filename}")
    except Exception as e:
        print(f"[ERROR] Error downloading {url}: {e}")

# Get all photos
all_photos = []
continuation_token = None

while True:
    data = get_photos(GAME, continuation_token)
    results = data.get('results', [])
    if not results:
        break
    all_photos.extend(results)

    paging_info = data.get('pagingInfo', {})
    continuation_tokens = paging_info.get('continuationTokens', [])
    if not continuation_tokens:
        break
    continuation_token = continuation_tokens[0]  # Use the first one for next page

print(f"Found {len(all_photos)} photos")



print("[INFO] Starting image download process...")
downloaded_count = 0
skipped_count = 0
error_count = 0

for i, photo in enumerate(all_photos):
    # Try to get the best quality available
    photo_cdn_path = photo.get('photoCdnPath')
    # If API provides other quality fields, prefer them (e.g. 'originalUrl', 'highResUrl')
    for key in ['originalUrl', 'highResUrl', 'cdnPath', 'url']:
        if photo.get(key):
            photo_cdn_path = photo[key]
            break
    if photo_cdn_path:
        filename = get_unique_filename(photo, i)
        before = os.path.exists(os.path.join("Downloads", filename))
        try:
            download_image(photo_cdn_path, filename)
            after = os.path.exists(os.path.join("Downloads", filename))
            if not before and after:
                downloaded_count += 1
            else:
                skipped_count += 1
        except Exception:
            error_count += 1
    else:
        print(f"[ERROR] No photoCdnPath for photo {i+1}")
        error_count += 1

print(f"[SUMMARY] Downloaded: {downloaded_count}, Skipped: {skipped_count}, Errors: {error_count}")
print("[INFO] Download process complete!")

print("Download complete!")