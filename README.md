# ETL Pipeline on Light Duty Electric Drive Vehicles Monthly Sales.

## Table of Contents

- [Overview](#overview)
- [Data Source](#data-source)
- [Tech Stack & Infrastructure](#tech-stack--infrastructure)
- [Manual Steps to Run the Application](#manual-steps-to-run-the-application)
- [Authors](#authors)

## Overview

This project implements a custom Python-based ETL pipeline to automate the extraction, transformation, and loading of monthly sales data for light-duty electric drive vehicles from the **anl.gov** website. Using Selenium in `headless=False` mode due to the site’s incompatibility with headless operation, the pipeline downloads the latest PDF report, parses it to extract structured sales information, applies data cleaning and transformation for consistency, and uploads the processed dataset to AWS S3 for secure storage and further analysis.

## Data Source

[Light Duty Electric Drive Vehicles Monthly Sales Updates - Historical Data](https://www.anl.gov/esia/reference/light-duty-electric-drive-vehicles-monthly-sales-updates-historical-data)

## Tech Stack & Infrastructure

1. Python
2. Selenium
3. Docker
4. GitHub Actions
5. Amazon S3
6. Amazon Elastic Container Registry

## Manual Steps to Run the Application

#### Step 1: Export the Environment Variables to Run the Application.

```bash
=========================================================================
Paste the following credentials as environment variables.
=========================================================================

# Export the Environment Variables inside the .env file.
AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXXX"
AWS_REGION_NAME="ap-south-1"
AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
S3_BUCKET_NAME="aws-s3-bucket-name"

# Set the Environment Variables inside GitHub Actions Secrets.
AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
AWS_REGION: ${{ secrets.AWS_REGION }}
AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
ECR_REPOSITORY_NAME: ${{ secrets.ECR_REPOSITORY_NAME }}
S3_BUCKET_NAME: ${{ secrets.S3_BUCKET_NAME }}
```

#### Step 2: Setup AWS S3 & ECR to store artifacts and Docker images.

- **AWS S3 to store project artifacts and log files.**
- **AWS ECR to store Docker images.**

#### Step 3: Manual Steps to Run the Application in a Local System.

```bash
# Create a Virtual Environment.
python -m venv venv

# Activate the Virtual Environment.
venv\Scripts\Activate.ps1

# Install the Dependencies.
python.exe -m pip install --upgrade pip
pip install -r requirements\requirements.in

# Generate the requirements.txt file.
inv req-compile

# Run the linter to verify the code structure with PEP8.
inv lint

# Install the Python packages.
pip install .

# Run the Console Script.
run_anl_ev_sales_etl
```

#### Step 4: Manual Steps to Run the Application in Docker.

- **Docker Build Command.**
  ```bash
  docker build -t <image-name>:latest .
  ```
- **Docker Run Command.**

  ```bash
  docker run -it --rm --cpus="0.5" -m 512m \
    -e AWS_ACCESS_KEY_ID=<AWS-ACCESS-KEY-ID> \
    -e AWS_SECRET_ACCESS_KEY=<AWS-SECRET-ACCESS-KEY> \
    -e AWS_REGION_NAME=<AWS-REGION-NAME> \
    -e S3_BUCKET_NAME=<S3-BUCKET-NAME> \
    <image-name>:latest /bin/bash

  >> xvfb-run --auto-servernum --server-num=1 run_anl_ev_sales_etl
  ```

## Authors

- [Aritra Ganguly](https://in.linkedin.com/in/gangulyaritra)
