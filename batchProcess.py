import csv
import re
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from percy import percy_snapshot

CSV_FILE = "./urls.csv"
NUM_THREADS = 2

def load_urls():
    with open(CSV_FILE, newline="") as file:
        reader = csv.reader(file)
        return [
            row[0].strip()
            for row in reader
            if row and row[0].strip().startswith(("http://", "https://"))
        ]

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [
        lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
        for i in range(n)
    ]

def get_snapshot_name(url):
    parsed = urlparse(url)
    hostname = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/")
    sanitized_path = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        path
    )
    if sanitized_path:
        return f"{hostname}_{sanitized_path}"
    return hostname

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)
    return driver

def process_urls(urls):
    if not urls:
        return
    driver = create_driver()
    try:
        for url in urls:
            try:
                print(f"Loading URL: {url}")
                driver.get(url)
                sleep(3)
                snapshot_name = get_snapshot_name(url)
                print(f"Taking Percy snapshot: {snapshot_name}")
                percy_snapshot(
                    driver,
                    snapshot_name,
                    widths=[768, 1200]
                )
                print(f"Snapshot completed: {snapshot_name}")
            except Exception as e:
                print(f"Failed for URL: {url}")
                print(str(e))
    finally:
        driver.quit()

def main():
    urls = load_urls()
    if not urls:
        print("No URLs found in urls.csv")
        return
    print(f"Found {len(urls)} URLs")
    print(f"Using {NUM_THREADS} parallel threads")
    batches = split_list(urls, NUM_THREADS)
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [
            executor.submit(process_urls, batch)
            for batch in batches
            if batch
        ]
        for future in futures:
            future.result()
    print("All snapshots completed")

if __name__ == "__main__":
    main()