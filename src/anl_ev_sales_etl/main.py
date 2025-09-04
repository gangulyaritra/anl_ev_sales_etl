import os
import time

import pandas as pd
import pdfplumber
from memory_profiler import profile

from anl_ev_sales_etl.utils.base_classes import DataExtractor
from anl_ev_sales_etl.utils.helper_functions import (
    convert_month,
    convert_value,
    extract_file_names_from_folder,
    is_file_downloaded,
    is_page_loaded,
    scroll_and_click_element,
)


class EVMonthlySalesETL(DataExtractor):
    URL = "https://www.anl.gov/esia/reference/light-duty-electric-drive-vehicles-monthly-sales-updates-historical-data"

    COLS = ["date", "BEV", "PHEV", "HEV", "TotalLDV"]

    @staticmethod
    def selenium_url_extraction(driver, url: str) -> str:
        """
        Extracts the URL of the PDF file from the webpage using Selenium.
        :param driver: Selenium WebDriver instance.
        :param url: The URL of the webpage to scrape.
        :return: The URL of the PDF file.
        """
        xpath = "/html/body/div[2]/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div/a"
        driver.get(url)

        while not is_page_loaded(driver=driver, xpath=xpath):
            EVMonthlySalesETL.logger.info("Page did not load properly. Reloading...")
            driver.refresh()

        scroll_and_click_element(driver=driver, xpath=xpath)

        return driver.current_url

    @staticmethod
    def extract_tables_from_pdf(pdf_path: str):
        """
        Extracts tables from a PDF file and returns them as a DataFrame.
        :param pdf_path: Path to the PDF file.
        :return: A DataFrame containing the extracted data.
        """
        dataframes = []
        combined_df = pd.DataFrame()

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=EVMonthlySalesETL.COLS)
                    dataframes.append(df)

        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)

        combined_df = combined_df.iloc[1:]
        return combined_df.reset_index(drop=True)

    def extract(self):
        self.logger.info("Initiating the Data Extraction Method.")

        if not os.path.exists(self.base_variables.download_path):
            os.makedirs(self.base_variables.download_path)

        self.logger.info("Starting the Selenium Automation.")
        pdf_url = self.selenium_url_extraction(
            driver=self.selenium_handler.driver, url=EVMonthlySalesETL.URL
        )
        self.selenium_handler.driver.get(pdf_url)

        self.logger.info("Waiting for the file to get downloaded...")
        while not is_file_downloaded(self.base_variables.download_path):
            time.sleep(10)

        self.logger.info(
            "File downloaded successfully to %s", self.base_variables.download_path
        )

        self.selenium_handler.driver.quit()
        self.logger.info("Selenium Automation Completed.")

    def transform(self):
        self.logger.info("Initiating the Data Transformation Method.")

        df = self.extract_tables_from_pdf(
            pdf_path=os.path.join(
                self.base_variables.download_path,
                extract_file_names_from_folder(self.base_variables.download_path)[0],
            )
        )

        df = df.apply(lambda col: col.map(convert_value))
        df.loc[:, "date"] = df["date"].apply(convert_month)
        df["date"] = pd.to_datetime(df["date"])
        df[EVMonthlySalesETL.COLS[1:]] = (
            df[EVMonthlySalesETL.COLS[1:]]
            .apply(pd.to_numeric, errors="coerce")
            .astype(int)
        )

        melted_df = pd.melt(
            df,
            id_vars=["date"],
            value_vars=EVMonthlySalesETL.COLS[1:],
            var_name="series_id",
            value_name="value",
        )
        melted_df["series_id"] = melted_df["series_id"].str.lower()

        self.df = melted_df[["series_id", "date", "value"]]

        self.df = self.df.merge(self.metadata_df, on="series_id", how="left")


@profile
def main():
    obj = EVMonthlySalesETL()
    obj.etl()
