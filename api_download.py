import requests
import json
import os
from urllib.parse import urljoin

# Configuration
API_BASE_URL = "https://api.forza.net"
ACCESS_TOKEN = "hbriwyHF7kQhZoZRSVWDsG2rlM3VJAIC4Pg_T4K4Jsk"  # Replace with your actual token
GAME = "FH5"  # or "FM", "FH4", "FM7"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Directory to save images
os.makedirs("high_res_images", exist_ok=True)

def get_photos(game, continuation_token=None):
    url = f"{API_BASE_URL}/api/v4/me/gallery/{game}"
    if continuation_token:
        url += f"?continuationToken={continuation_token}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join("high_res_images", filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

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

# Download high-res images
for i, photo in enumerate(all_photos):
    photo_cdn_path = photo.get('photoCdnPath')
    if photo_cdn_path:
        title = photo.get('title', f'photo_{i+1}').replace('/', '_').replace('\\', '_')
        filename = f"{title}.jpg"  # Assume JPG, adjust if needed
        download_image(photo_cdn_path, filename)
    else:
        print(f"No photoCdnPath for photo {i+1}")

print("Download complete!")