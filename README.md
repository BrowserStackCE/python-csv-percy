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

### Step 1: Create a Python virtual environment

It's recommended to create a virtual environment to manage dependencies isolated from your system Python.

```bash
python3 -m venv venv
source venv/bin/activate 
```

### Step 2: Install Percy CLI via npm

The Percy CLI is needed to capture and upload snapshots. Install it via npm:

```bash
npm install
```

### Step 3: Install Python dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip3 install -r requirements.txt
```

## Usage

### Step 1: Update the `urls.csv` file

This file contains all the URLs you need to capture using Percy.

### Step 2: Run the file to capture snapshots using Percy

Export the Percy Token located in your project settings of Percy and then run the python command to initiate the execution.

```bash
export PERCY_TOKEN=your-percy-token
npx percy exec -- python3 batchProcess.py
```