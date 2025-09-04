import os
from datetime import datetime
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def is_page_loaded(driver: WebDriver, xpath: str, timeout: int = 10) -> bool:
    """
    Check if the page has loaded correctly by waiting for a specific element to be present.
    :param driver: The Selenium WebDriver instance.
    :param xpath: The XPath of the element to wait for.
    :param timeout: The maximum time to wait for the element to be present.
    :return: True if the element is present, False if a TimeoutException occurs.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except TimeoutException:
        return False


def scroll_and_click_element(driver: WebDriver, xpath: str, timeout: int = 10) -> None:
    """
    Scroll to an element and click it using Selenium WebDriver.
    :param driver: The Selenium WebDriver instance.
    :param xpath: The XPath of the element to scroll to and click.
    :param timeout: The maximum time to wait for the element to be clickable.
    :return: None
    """
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
    """
    Convert a string value by stripping whitespace and removing spaces and commas.
    :param value: The string value to convert.
    :return: The converted string value.
    """
    return value.strip().replace(" ", "").replace(",", "")


def convert_month(date_str: str) -> str:
    """
    Convert a date string in the format "MM-YY" to "YYYY-MM-01".
    :param date_str: The date string in the format "MM-YY".
    :return: The converted date string in the format "YYYY-MM-01".
    """
    return datetime.strptime(date_str, "%b-%y").strftime("%Y-%m-01")


def is_file_downloaded(download_path: str) -> bool:
    """
    Check if a file has been downloaded to the specified path.
    :param download_path: The path where the file is expected to be downloaded.
    :return: True if a file is found in the download path, False otherwise.
    """
    if not os.path.exists(download_path):
        raise FileNotFoundError(f"Download path does not exist: {download_path}")

    return len(os.listdir(download_path)) == 1


def extract_file_names_from_folder(folder_path: str) -> List[str]:
    """
    Extract file names from the specified folder path.
    :param folder_path: The path to the folder from which to extract file names.
    :return: A list of file names in the specified folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder path does not exist: {folder_path}")

    return [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
