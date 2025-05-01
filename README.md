# ETL Pipeline on Light Duty Electric Drive Vehicles Monthly Sales.

## Introduction.

Build a custom ETL pipeline in Python to extract monthly sales data for light-duty electric drive vehicles from the **anl.gov** website.

## Data Scrape.

[Light Duty Electric Drive Vehicles Monthly Sales Updates - Historical Data](https://www.anl.gov/esia/reference/light-duty-electric-drive-vehicles-monthly-sales-updates-historical-data)

## Export the Environment Variables inside the .env file.

```bash
=========================================================================
Paste the following credentials as environment variables.
=========================================================================

AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXXX"
AWS_REGION_NAME="ap-south-1"
AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
S3_BUCKET_NAME="aws-s3-bucket-name"
```

## Manual Steps to Run the Application on Windows.

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

# Automate the Trigger.
run_anl_ev_sales_etl
```

## Manual Steps to Run the Application on Docker.

- **Docker Build Command.**
  ```bash
  docker build -t <image-name>:latest .
  ```
- **Docker Run Command.**

  ```bash
  docker run -it --rm --cpus="1.0" -m 512m \
    -e AWS_ACCESS_KEY_ID=<AWS-ACCESS-KEY-ID> \
    -e AWS_SECRET_ACCESS_KEY=<AWS-SECRET-ACCESS-KEY> \
    -e AWS_REGION_NAME=<AWS-REGION-NAME> \
    -e S3_BUCKET_NAME=<S3-BUCKET-NAME> \
    <image-name>:latest /bin/bash

  >> xvfb-run --auto-servernum --server-num=1 run_anl_ev_sales_etl
  ```

## Authors

- [Aritra Ganguly](https://in.linkedin.com/in/gangulyaritra)

## License & Copyright

[MIT License](LICENSE)
