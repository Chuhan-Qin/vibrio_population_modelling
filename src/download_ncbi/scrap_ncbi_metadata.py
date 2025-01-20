from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import re
from Bio import Entrez
from Bio import SeqIO
from torch import unique


def fetch_metadata(accession):
    # Initiate WebDriver
    driver = webdriver.Chrome()
    url = f"https://www.ncbi.nlm.nih.gov/datasets/genome/{accession}/"

    try:
        # Fetch HTML content from NCBI
        driver.get(url)

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'maincontent')))

        # Parse the HTML content
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        # Find the section containing isolate metadata
        metadata_section = soup.find('h2', string='Sample details')
        if not metadata_section:
            raise Exception('Sample details not found')

        # Extract and clean text from the metadata section
        # Store the extracted information to a dictionary
        meta_dict = {}

        if metadata_section:
            # Get the content under 'Sample details'
            metadata_content = metadata_section.find_next('div')
            if metadata_content:
                meta_lst = metadata_content.get_text('\n', strip=True).split('\n')
                for i in range(0, len(meta_lst), 2):
                    meta_dict[meta_lst[i]] = meta_lst[i+1]
                return meta_dict

            else:
                print(f'Sample details for accession {accession} are empty.')

    finally:
        driver.quit()


def retrieve_accession_by_taxid(taxid: str, page_max: int):
    # Set up the Selenium web driver and get the page
    driver = webdriver.Chrome()
    url = f'https://www.ncbi.nlm.nih.gov/datasets/genome/?taxon={taxid}'
    driver.get(url)
    refseq_ids = []
    page_counter = 1  # Start from the first page

    try:
        while page_counter <= page_max:
            # Wait until GCF_ IDs are visible on the page
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'GCF_')]"))
            )
            print(f"All RefSeq IDs are loaded for page {str(page_counter)}.")

            # Extract RefSeq IDs from the current page
            response = driver.page_source
            soup = BeautifulSoup(response, 'html.parser')

            temp_ids = soup.find_all(string=re.compile(r"GCF_\d+"))
            unique_refseq_ids = list(set(temp_ids))
            refseq_ids.extend(unique_refseq_ids)

            # Check if a "Next" button exists and is clickable
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='next page' and @data-ga-label='next_page']")
                    )
                )
                next_button.click()  # Click the next button
                page_counter += 1

            except Exception as e:
                print("No more pages to process or 'Next' button not found.")
                break  # Exit the loop if the next button is not found

    finally:
        print(f'Finished processing all {str(page_max)} pages.\nNow quitting the browser.')
        driver.quit()

    return refseq_ids


