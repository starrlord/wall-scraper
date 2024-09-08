# Wall-Scraper

`wall-scraper` is a Python-based command-line tool that automates downloading high-resolution wallpapers from websites. It supports scraping images from multiple pages of wallpaper galleries and saves them in a specified directory.

## Features

- Scrapes wallpaper images from user-defined websites.
- Supports downloading from multiple pages.
- Automatically saves wallpapers in a user-specified directory.
- Randomized user-agent selection to avoid request blocks.
- Retry mechanism for handling 429 (Too Many Requests) errors.

## Requirements

- Python 3.x
- Required Python Libraries: `requests`, `beautifulsoup4`, `argparse`

Install the required libraries using the following command:

```bash
pip install requests beautifulsoup4
```

## Usage

To run the script, use the following command format:

```bash
python wall-scrape.py --saveto <directory_path> --url <website_url> --pages <number_of_pages> [--dir_name <subdirectory_name>]
```

### Example:

```bash
python wall-scrape.py --saveto "D:/wallpapers/" --url "https://wallpaperscraft.com/tag/pumpkins/3840x2160" --pages 5 --dir_name "halloween"
```

This command will:

- Save wallpapers to the `D:/temp/wallpapers/` directory.
- Scrape wallpaper images from the given URL across 5 pages.
- Save images into the `halloween` subdirectory.

### Arguments:

- `--saveto` (required): The base directory where wallpapers will be saved.
- `--url` (required): The base URL of the wallpaper site to scrape images from.
- `--pages` (required): The number of pages to scrape images from.
- `--dir_name` (optional): The name of the sub-directory to save wallpapers. Defaults to `wallpapers`.

### Additional Information:

- The scraper tries multiple strategies to locate the highest resolution wallpaper available on the page.
- The script uses a randomized user-agent list to mimic browser-like requests, reducing the chances of being blocked.
- If the server responds with a 429 error, the script will automatically retry after an exponential backoff.

## License

This project is licensed under the MIT License.
