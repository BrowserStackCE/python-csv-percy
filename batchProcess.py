import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from percy import percy_snapshot
from time import sleep
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = './urls.csv'  # Path to your CSV file
NUM_THREADS = 5  # Number of parallel threads
CHROMEDRIVER_PATH = "./chromedriver"

# Load URLs from CSV
def load_urls():
    with open(CSV_FILE, newline='') as file:
        reader = csv.reader(file)
        return [row[0].strip() for row in reader if row[0].strip().startswith(("http://", "https://"))]

# Function for each thread to process its batch of URLs
def process_urls(urls):
    if not urls:
        print("No URLs provided to process.")
        return
    
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service) 
    try:
        for url in urls:
            print(f"Loading URL: {url}")
            driver.get(url)
            sleep(2) 

            # Capture Percy snapshot
            snapshot_name = f"Snapshot for {url}"
            print(f"Capturing Percy snapshot: {snapshot_name}")
            percy_snapshot(driver, snapshot_name)
    finally:
        driver.quit()  # Ensure the driver closes after the batch is done

def main():
    urls = load_urls()
    
    # Split URLs into batches based on the number of threads
    batch_size = len(urls) // NUM_THREADS
    url_batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

    # Process each batch in parallel
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(process_urls, batch) for batch in url_batches]
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
