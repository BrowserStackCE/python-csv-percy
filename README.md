# Percy Batch URL Snapshotter

This project uses Selenium and Percy to capture visual snapshots of multiple URLs in batches using Python. By leveraging parallel threading, it efficiently processes large lists of URLs, uploading snapshots to Percy for visual testing.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)

## Prerequisites

- **Python**: Version 3.7 or higher
- **Percy CLI**: Required for snapshot uploading (see installation steps below)
- **ChromeDriver**: Ensure it matches your installed Chrome version
- **Percy Account**: [Sign up for a Percy account](https://percy.io) to get your project token

## Setup

### Step 1: Install Percy CLI via npm

The Percy CLI is needed to capture and upload snapshots. Install it via npm:

```bash
npm install
```

### Step 2: Install Python dependencies


```bash
pip3 install -r requirements.txt
```


## Usage

### Step 1: Update the `urls.csv` file

This file contains all the URLs you need to capture using Percy.

### Step 2: Update the `CHROMEDRIVER_PATH` variable in `batchProcess.py` file

This will point the selenium test to your chromedrive to successfully launch the Chrome Browser. You can also update the variable `NUM_THREADS` if you want to increase the number of parallel threads.

###  Step 3: Run the file to capture snapshots using Percy.

Export the Percy Token located in your project settings of Percy and then run the python command to initiate the execution.

```bash
export PERCY_TOKEN=your-percy-token
npx percy exec -- python3 batchProcess.py
```





