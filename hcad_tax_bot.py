"""
Description:
    This script is a web scraper for property tax data from Harris County, Texas.
        1. Use an inputted address to look up Harris Country Appraisal District (HCAD) account numbers from https://hcad.org
        2. Use account numbers to find property tax data from https://www.hctax.net
        3. Output property tax data to a csv file
Written by:
    G-R-H
"""

# Import necessary packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd

year = input("Enter a year between 2015-2020: ")
street_name = input("Enter your Street Name: ")


class HCPropertyBot():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)

    def property_search(self):
        """ Searches for properties on a given street"""

        self.driver.get('https://public.hcad.org/records/Real.asp?search=addr')

        yr_sel = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[3]/td[1]/form/select')
        Select(yr_sel).select_by_value(year)

        street_name_in = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[3]/td[3]/input')
        street_name_in.send_keys(street_name)

        similar_box = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[3]/td[4]/input[1]')
        if not similar_box.is_selected():
            similar_box.click()

        search_btn = self.driver.find_element_by_xpath("//input[@type='submit' and @value='Search']")
        search_btn.click()

    def save_properties(self):
        """ Saves properties into a DataFrame """

        rows = len(self.driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr')) # of rows
        cols = len(self.driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td')) # of cols

        list_of_rows = []

        # Loop through each row in the table
        for r in range(1, rows + 1):
            list_of_cells = []

            # Loop through each column in the table
            for c in range(1, cols + 1):
                value = self.driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[" + str(r) + "]/td[" + str(c) + "]").text
                list_of_cells.append(value)
            list_of_rows.append(list_of_cells)

        # Store property data in a DataFrame
        df = pd.DataFrame(list_of_rows)
        # Establish new header for the DataFrame
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header

        return df

    def lookup_taxes(self):
        """ Looks up the taxes due for the given account numbers """

        self.property_search()

        df = self.save_properties()

        taxes = []

        # Loop through each account number and perform a property tax record search
        for index, row in df.iterrows():
            self.driver.get('https://www.hctax.net/Property/PropertyTax')

            search_type_sel = self.driver.find_element_by_xpath('//*[@id="selTaxSearch"]')
            Select(search_type_sel).select_by_value('account')

            acct_num_in = self.driver.find_element_by_xpath('//*[@id="txtSearchValue"]')
            acct_num_in.clear()
            acct_num_in.send_keys(row['Account Number'])

            tax_search_btn = self.driver.find_element_by_xpath('//*[@id="btnSubmitTaxSearch"]')
            tax_search_btn.click()

            try:
                wait = WebDriverWait(self.driver, 15)
                wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/fieldset/div/div[2]/table/tbody/tr/td[1]/a')))
                acct_num_link = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/fieldset/div/div[2]/table/tbody/tr/td[1]/a')
                acct_num_link.click()
                amt_due = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/fieldset/div[3]/table[4]/tbody/tr[1]/td[2]').text
                taxes.append(amt_due)
            except NoSuchElementException:
                due = "N/A"
                taxes.append(due)
            except TimeoutException:
                due = "N/A"
                taxes.append(due)

        df[year + " Taxes Due"] = taxes

        # Create file to store output
        df.to_csv("property_taxes.csv")

        self.driver.close()


bot = HCPropertyBot()
bot.lookup_taxes()