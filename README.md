# SWD Scraper

A simple Python script that automatically logs into the SWD portal and fetches hostel data for each hostel available. This script uses web scraping techniques with `BeautifulSoup` and `requests` to extract and save the data to  JSON file.

## Features
- Automatically logs into the SWD portal using your credentials.
- Fetches and scrapes hostel data from the search page.
- Extracts relevant data and saves it in a JSON file.
- Iterates through all available hostel options and collects data from each one.

## Prerequisites

- Python 3.x
- `requests` 
- `beautifulsoup4` 
- `dotenv` 
You can install the necessary libraries using `pip`:

```bash
pip install requests beautifulsoup4 python-dotenv
```

## Usage

1. Clone this repository or download the script to your local machine.
2. Create a `.env` file in the same directory as the script and add your SWD credentials:

```plaintext
swd_id=your_username
swd_pwd=your_password
```
