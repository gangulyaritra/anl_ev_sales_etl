import os
from datetime import datetime
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def is_page_loaded(driver: WebDriver, xpath: str, timeout: int = 10) -> bool:
    # Function to check if the page has loaded correctly.
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except TimeoutException:
        return False


def scroll_and_click_element(driver: WebDriver, xpath: str, timeout: int = 10) -> None:
    # Scroll to the element.
    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        ),
    )

    # Click the element.
    driver.execute_script(
        "arguments[0].click();",
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ),
    )


def convert_value(value: str) -> str:
    # Strip whitespace and remove spaces and commas from the given string.
    return value.strip().replace(" ", "").replace(",", "")


def convert_month(date_str: str) -> str:
    # Convert a date string in the format "MMM-YY" to "YYYY-MM-01".
    return datetime.strptime(date_str, "%b-%y").strftime("%Y-%m-01")


def is_file_downloaded(download_path: str) -> bool:
    # Check if a file has been downloaded to the specified path.
    if not os.path.exists(download_path):
        raise FileNotFoundError(f"Download path does not exist: {download_path}")

    return len(os.listdir(download_path)) == 1


def extract_file_names_from_folder(folder_path: str) -> List[str]:
    # Extract file names from the specified folder path.
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder path does not exist: {folder_path}")

    return [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
