#!/usr/bin/env python3
"""
Foza Picture Downloader
A script to scrape and download high-resolution photos from Forza.net gallery.
"""

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def save_cookies(driver, cookies_file='cookies.json'):
    """Save cookies from browser to JSON file."""
    cookies = driver.get_cookies()
    with open(cookies_file, 'w') as f:
        json.dump(cookies, f, indent=4)
    print(f"Cookies saved to {cookies_file}")

def load_cookies(driver, cookies_file='cookies.json'):
    """Load cookies from JSON file into the browser."""
    if not os.path.exists(cookies_file):
        print(f"Cookies file {cookies_file} not found.")
        return False
    
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)
    
    cookies_loaded = 0
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
            cookies_loaded += 1
        except Exception as e:
            print(f"Error adding cookie {cookie.get('name', 'unknown')}: {e}")
    print(f"Total cookies loaded: {cookies_loaded}")
    return True

def download_image(url, filename):
    """Download image from URL to filename."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    # Setup Chrome options
    chrome_options = Options ()
    #chrome_options.add_argument("--headless")  # Run in headless mode, remove if you want to see the browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # You may need to specify the path to chromedriver
    # service = Service('/path/to/chromedriver')
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Forza gallery
        driver.get('https://forza.net/myforza')
        
        # Try to load saved cookies
        cookies_loaded = load_cookies(driver)
        if cookies_loaded:
            driver.refresh()
            time.sleep(3)
        
        # Check if logged in (if no cookies or still on login page)
        if not cookies_loaded or "login" in driver.current_url.lower() or "signin" in driver.current_url.lower():
            print("Not logged in. Please log in manually in the browser window.")
            print("Once logged in and on the gallery page, press Enter here to continue...")
            input("Press Enter to continue after logging in...")
            
            # Save cookies after login
            save_cookies(driver)
        
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Assume user has switched to grid view manually
        print("Assuming grid view is active. Proceeding to find images...")
        
        page_num = 1
        downloaded_count = 0
        
        while True:
            print(f"Processing page {page_num}...")
            
            # Find all image thumbnails (images with gallery URLs)
            images = driver.find_elements(By.CSS_SELECTOR, "img[src*='galleryv2images']")
            print(f"Found {len(images)} gallery images on page {page_num}.")
            
            for i, img in enumerate(images):
                try:
                    img_url = img.get_attribute('src')
                    print(f"Processing image {downloaded_count + i + 1}: {img_url}")
                    
                    # Change to high-res (/6 instead of /4)
                    if '/4' in img_url:
                        high_res_url = img_url.replace('/4', '/6')
                    else:
                        high_res_url = img_url  # Assume already high-res
                    
                    filename = f"downloads/photo_{downloaded_count + i + 1}.jpg"
                    download_image(high_res_url, filename)
                    
                except Exception as e:
                    print(f"Error processing image {downloaded_count + i + 1}: {e}")
            
            downloaded_count += len(images)
            
            # Try to go to next page
            try:
                # Look for next page button (div with specific class)
                next_button = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination-link') and contains(@class, 'page-up')]")
                if next_button.is_displayed() and next_button.get_attribute('aria-disabled') == 'false':
                    next_button.click()
                    # Wait for new images to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='galleryv2images']"))
                    )
                    time.sleep(2)  # Extra wait for all images
                    page_num += 1
                else:
                    print("Next button not clickable or disabled.")
                    break
            except Exception as e:
                print(f"No next page found: {e}")
                break
        
        print(f"Total images downloaded: {downloaded_count}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()