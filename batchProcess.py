import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from percy import percy_snapshot
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import re

CSV_FILE = './urls.csv'   # Path to your CSV file
NUM_THREADS = 2           # Number of parallel threads

# Load URLs from CSV
def load_urls():
    with open(CSV_FILE, newline='') as file:
        reader = csv.reader(file)
        return [row[0].strip() for row in reader if row and row[0].strip().startswith(("http://", "https://"))]

# Helper to split list into n even chunks
def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

# Function for each thread to process its batch of URLs
def process_urls(urls):
    if not urls:
        print("No URLs provided to process.")
        return
    # Use webdriver-manager to automatically install Chromedriver
    options = Options()
    options.add_argument("--headless=new")   # optional but recommended for Percy
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager(driver_version="139.0.7258.155").install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1200, 800)
    try:
        for url in urls:
            print(f"Loading URL: {url}")
            driver.get(url)
            sleep(2)

            parsed_url = urlparse(url)
            hostname = parsed_url.netloc
            if hostname.startswith("www."):
                hostname = hostname[4:]

            # Sanitize path: remove leading slash and replace other slashes with underscores
            path = parsed_url.path.lstrip('/')
            sanitized_path = re.sub(r'[^a-zA-Z0-9_-]', '_', path)  # Replace non-alphanum/underscore/dash chars

            # Construct snapshot name
            if sanitized_path:
                snapshot_name = f"Snapshot for {hostname}_{sanitized_path}"
            else:
                snapshot_name = f"Snapshot for {hostname}"

            print(f"Capturing Percy snapshot: {snapshot_name}")
            percy_snapshot(driver, snapshot_name,widths=[768, 1200])

    finally:
        driver.quit()

def main():
    urls = load_urls()
    if not urls:
        print("No URLs found in the CSV file.")
        return
    
    url_batches = split_list(urls, NUM_THREADS)

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Submit only non-empty batches
        futures = [executor.submit(process_urls, batch) for batch in url_batches if batch]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
