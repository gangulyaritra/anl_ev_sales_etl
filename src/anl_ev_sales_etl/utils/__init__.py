import argparse
import os
from pathlib import Path

import pandas as pd

from anl_ev_sales_etl.utils.selenium_tools import Selenium

DOWNLOAD_PATH = os.path.join(os.getenv("DOWNLOAD_DIR", os.getcwd()), "ev_sales")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "anl-us-ev-sales")

ANL_METADATA = pd.read_json(
    Path(__file__).parent / "anl_ev_sales_metadata.json", orient="index"
)


# Initiate all the handlers here.
SELENIUM_HANDLER = Selenium(
    headless=False,
    downloads_path=DOWNLOAD_PATH,
    prefs={
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)


def parse_args() -> argparse.Namespace:
    """
    Argument parser

    Returns:
        Args: an argparse object
    """

    parser = argparse.ArgumentParser(description="Parameters for ETL")

    # Add argument for environment.
    parser.add_argument(
        "--environment",
        help="Which environment to run the project in?",
        default="uat",
        choices=["uat", "prod"],
    )

    args, _ = parser.parse_known_args()

    pfx = "anl\\us_vehicle_sales"
    args.sj_prefix = pfx if args.environment == "prod" else f"uat\\{pfx}"

    return args


parsed_args = parse_args()
