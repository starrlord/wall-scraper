#Run Command:  python scrape.py --saveto "D:/temp/wallpapers/" --url "https://wallpaperscraft.com/tag/pumpkins/3840x2160" --pages 5 --dir_name "halloween"

import requests
from bs4 import BeautifulSoup as sp
from os import mkdir, chdir, path
import argparse
import uuid
import random
import time
from urllib.parse import urlparse

# User-Agent list to randomize requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]


def fetch_page(url):
    """Fetch a page."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return None


def fetch_image(link):
    """Fetch the wallpaper image link from the page, trying multiple strategies."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        re1 = requests.get(link, headers=headers)
        re1.raise_for_status()
        soup1 = sp(re1.content, "html.parser")

        # Strategy 1: Look for the direct download button with 'gui-button_full-height' class
        download_link_tag = soup1.select_one('a.gui-button.gui-button_full-height')
        if download_link_tag and download_link_tag.get("href"):
            return download_link_tag["href"]

        # Strategy 2: Look for the JS Popup element
        popup_link_tag = soup1.select_one('a.JS-Popup')
        if popup_link_tag and popup_link_tag.get("href"):
            return popup_link_tag["href"]

        # Strategy 3: Check for the wallpaper image directly in 'img.wallpaper__image'
        img_tag = soup1.select_one("img.wallpaper__image")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]

        # If none of the strategies work, raise an error
        raise ValueError("No valid download link or image found on this page")

    except Exception as e:
        print(f"Error fetching image from {link}: {e}")
        return None


def find_pics(base_url, pages):
    """Find wallpaper images across multiple pages."""
    pics = []
    for page in range(1, pages + 1):
        url = f"{base_url}/page{page}"  # Assuming pages follow a predictable format
        page_content = fetch_page(url)
        if page_content:
            soup = sp(page_content, "html.parser")
            x = soup.select("li.wallpapers__item > a:nth-child(1)")
            links = ["https://wallpaperscraft.com" + str(i["href"]) for i in x]

            for link in links:
                pic = fetch_image(link)
                if pic and "x" in pic.split('/')[-1]:  # Check for resolution in URL
                    pics.append(pic)

    return pics


def get_filename_from_url(url):
    """Extract the original filename including the resolution from the URL."""
    parsed_url = urlparse(url)
    # Extract the last part of the path that includes the resolution
    file_name = parsed_url.path.split('/')[-1]  # This part includes the resolution (e.g., 'halloween_pumpkin_glow_190219_3840x2160')
    return file_name


def download_image(pic, idx):
    """Download a single image with retry logic for 429 errors."""
    retries = 5  # Set a max number of retries
    delay = 2  # Start with a delay of 10 seconds for retrying
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    for attempt in range(retries):
        try:
            response = requests.get(pic, headers=headers, stream=True)
            if response.status_code == 429:  # Too Many Requests
                print(f"429 Too Many Requests, retrying after {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                continue  # Retry the request
            response.raise_for_status()

            # Get the filename from the URL (which includes the resolution)
            image_filename = get_filename_from_url(pic)
            
            with open(image_filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded {image_filename}")
            time.sleep(2)  # Pause for 2 seconds between downloads
            break  # Exit loop if successful
        except Exception as e:
            print(f"Failed to download {pic}: {e}")
            if attempt == retries - 1:
                print("Max retries reached. Skipping...")


def download_pics(pics):
    """Download all wallpaper images sequentially with a delay."""
    for idx, pic in enumerate(pics):
        download_image(pic, idx)


def make_dir(download_dir, dir_name):
    """Create the download directory if it doesn't exist and switch to it."""
    target_dir = path.join(download_dir, dir_name)
    if not path.exists(target_dir):
        mkdir(target_dir)
    chdir(target_dir)


def main():
    parser = argparse.ArgumentParser(description="Wallpaper Downloader Script")
    parser.add_argument("--saveto", type=str, required=True, help="Base directory to save wallpapers")
    parser.add_argument("--url", type=str, required=True, help="Base URL of the wallpaper site")
    parser.add_argument("--pages", type=int, required=True, help="Number of pages to download")
    parser.add_argument("--dir_name", type=str, required=False, default="wallpapers", help="Sub-directory name to save wallpapers")

    args = parser.parse_args()

    # Create or switch to the target directory
    make_dir(args.saveto, args.dir_name)

    # Find and download wallpapers
    pics = find_pics(args.url, args.pages)
    if not pics:
        print("No wallpapers were found to download.")
    else:
        print(f"Found {len(pics)} images.")
        download_pics(pics)


if __name__ == "__main__":
    main()
