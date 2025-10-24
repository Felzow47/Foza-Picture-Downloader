# Foza Picture Downloader

A Python script to download high-resolution photos from your Forza.net gallery.

## Requirements

- Python 3.8+
- Microsoft/Xbox account with Forza access
- Chrome browser installed
- ChromeDriver (automatically managed by selenium)

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the script: `python main.py`
   - On first run, log in manually to your Microsoft/Xbox account.
   - Cookies will be saved automatically for future runs.
   - On subsequent runs, it will try to load cookies; if expired, log in again.

## Usage

The script will:

- Open the browser and prompt you to log in manually.
- After login, switch to grid view in the gallery.
- Return to the terminal and press Enter.
- Automatically find and download all high-resolution images to the `downloads` folder.

## Notes

- If no images are found, the selector may need adjustment based on the current Forza website structure.
- Images are downloaded by modifying thumbnail URLs (/4) to high-res (/6).
