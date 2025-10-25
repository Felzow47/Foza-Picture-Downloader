import json
import re
import os
import hashlib
import requests
from typing import List, Dict, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('har_downloader.log'),
        logging.StreamHandler()
    ]
)

class HARImageExtractor:
    def __init__(self, har_file_path: str):
        self.har_file_path = har_file_path
        self.downloaded_hashes: Set[str] = set()

    def load_har_file(self) -> Dict:
        """Load and parse the HAR file."""
        try:
            with open(self.har_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load HAR file: {e}")
            raise

    def extract_image_urls(self, har_data: Dict) -> List[str]:
        """Extract all photoCdnPath URLs from HAR responses."""
        image_urls = []

        for entry in har_data.get('log', {}).get('entries', []):
            response = entry.get('response', {})
            content = response.get('content', {})
            text = content.get('text', '')

            # Look for photoCdnPath in JSON responses
            if '"photoCdnPath":"' in text:
                # Extract all photoCdnPath URLs using regex
                photo_urls = re.findall(r'"photoCdnPath":"(https://[^"]+)"', text)
                image_urls.extend(photo_urls)

        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in image_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)

        logging.info(f"Extracted {len(unique_urls)} unique image URLs from HAR")
        return unique_urls

    def get_file_hash(self, filepath: str) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def load_existing_hashes(self, download_dir: str):
        """Load hashes of already downloaded files."""
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        for filename in os.listdir(download_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                filepath = os.path.join(download_dir, filename)
                try:
                    file_hash = self.get_file_hash(filepath)
                    self.downloaded_hashes.add(file_hash)
                except Exception as e:
                    logging.warning(f"Could not hash file {filepath}: {e}")

        logging.info(f"Loaded {len(self.downloaded_hashes)} existing file hashes")

    def download_image(self, url: str, download_dir: str) -> bool:
        """Download a single image if not already downloaded."""
        try:
            # Create download directory if it doesn't exist
            os.makedirs(download_dir, exist_ok=True)

            # Get filename from URL (use image_id from URL path)
            url_parts = url.split('/')
            filename = url_parts[-2] + '.jpg'  # Use second-to-last part (image_id) as filename

            # Clean filename
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            filepath = os.path.join(download_dir, filename)

            # Check if file already exists
            if os.path.exists(filepath):
                existing_hash = self.get_file_hash(filepath)
                if existing_hash in self.downloaded_hashes:
                    logging.info(f"Skipping already downloaded: {filename}")
                    return True
                else:
                    # File exists but hash not in set, might be duplicate
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(os.path.join(download_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    filepath = os.path.join(download_dir, f"{base}_{counter}{ext}")

            # Download the image
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                logging.warning(f"Skipping non-image content: {url} (content-type: {content_type})")
                return False

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            # Calculate hash and add to set
            file_hash = self.get_file_hash(filepath)
            self.downloaded_hashes.add(file_hash)

            logging.info(f"Downloaded: {filename}")
            return True

        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")
            return False

    def download_all_images(self, urls: List[str], download_dir: str = "har_downloaded_images") -> Dict[str, int]:
        """Download all images from the extracted URLs."""
        self.load_existing_hashes(download_dir)

        successful = 0
        failed = 0

        logging.info(f"Starting download of {len(urls)} images to {download_dir}")

        for i, url in enumerate(urls, 1):
            logging.info(f"Processing {i}/{len(urls)}: {url}")
            if self.download_image(url, download_dir):
                successful += 1
            else:
                failed += 1

        logging.info(f"Download complete. Successful: {successful}, Failed: {failed}")
        return {"successful": successful, "failed": failed, "total": len(urls)}

def main():
    har_file = "forza.net_Archive [25-10-25 00-41-40].har"
    download_dir = "har_downloaded_images"

    if not os.path.exists(har_file):
        logging.error(f"HAR file not found: {har_file}")
        return

    extractor = HARImageExtractor(har_file)

    try:
        # Load HAR data
        logging.info("Loading HAR file...")
        har_data = extractor.load_har_file()

        # Extract image URLs
        logging.info("Extracting image URLs...")
        image_urls = extractor.extract_image_urls(har_data)

        if not image_urls:
            logging.warning("No image URLs found in HAR file")
            return

        # Download images
        results = extractor.download_all_images(image_urls, download_dir)

        print("\nHAR Download Results:")
        print(f"Total URLs found: {results['total']}")
        print(f"Successfully downloaded: {results['successful']}")
        print(f"Failed downloads: {results['failed']}")
        print(f"Images saved to: {download_dir}")

    except Exception as e:
        logging.error(f"Error during processing: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()