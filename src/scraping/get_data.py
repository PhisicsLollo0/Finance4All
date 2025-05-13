from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from glob import glob
from datetime import datetime
import pandas as pd
import time
import os

from dotenv import load_dotenv
import os

load_dotenv()
INDEXES_DIR = os.getenv("INDEXES_DIR")

now = datetime.now()
current_date = now.strftime("%Y/%m")

def download_from_curvo(driver, file_name, url_curvo):

    # Go to the page
    driver.get(url_curvo)

    wait = WebDriverWait(driver, 20)
    export_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chart-button-export-as-csv")))

    # Step 3: Click the export button
    export_button.click()

    original_filename = "chart.csv"  # <-- this is the default downloaded name
    new_filename = file_name  # <-- whatever you want

    # Build full paths
    original_path = os.path.join(INDEXES_DIR, original_filename)
    new_path = os.path.join(INDEXES_DIR, new_filename)

    # Wait for the file to exist (extra safe)
    for _ in range(10):
        if os.path.exists(original_path):
            break
        time.sleep(1)

    # Rename
    if os.path.exists(original_path):
        os.rename(original_path, new_path)
        print(f"File downloaded and renamed to {new_path.split('/')[-1]}")
    else:
        print("Download failed or file not found.")

def start_up_scraping(curvo_indexes):

    # Set up options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.prompt_for_download": False,
        "download.default_directory": INDEXES_DIR,  # Change this to your download folder
        "profile.default_content_settings.popups": 0,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Launch browser
    driver = webdriver.Chrome(options=chrome_options)

    for i in range(len(curvo_indexes)):
        download_from_curvo(driver, *curvo_indexes[i])

    driver.quit()


def download_data_updated():        

    dict_indexes_on_curvo = [('MSCI_World.csv'                                  , 'https://curvo.eu/backtest/en/market-index/msci-world?currency=eur'),
                            ('MSCI_Europe_Small_Cap_Value_Weighted.csv'         , 'https://curvo.eu/backtest/en/market-index/msci-europe-small-cap-value-weighted?currency=eur'),
                            ('MSCI_Europe.csv'                                  , 'https://curvo.eu/backtest/en/market-index/msci-europe?currency=eur'),
                            ('MSCI_ACWI.csv'                                    , 'https://curvo.eu/backtest/en/market-index/msci-acwi?currency=eur'),
                            ('S&P_500_Minimum_Volatility.csv'                   , 'https://curvo.eu/backtest/en/market-index/sp-500-minimum-volatility?currency=eur'),
                            ('MSCI_Emerging_Markets.csv'                        , 'https://curvo.eu/backtest/en/market-index/msci-emerging-markets?currency=eur'),
                            ('FTSE_World_Government_Bond_Developed_Markets.csv' , 'https://curvo.eu/backtest/en/market-index/ftse-world-government-bond-developed-markets?currency=eur'),
                            ('S&P_500.csv'                                      , 'https://curvo.eu/backtest/en/market-index/sp-500?currency=eur'),
                            ('MSCI_USA_Small_Cap_Value_Weighted.csv'            , 'https://curvo.eu/backtest/en/market-index/msci-usa-small-cap-value-weighted?currency=eur'),
                            ('MSCI_World_Momentum.csv'                          , 'https://curvo.eu/backtest/en/market-index/msci-world-momentum?currency=eur'),
                            ]

    start_up_scraping(dict_indexes_on_curvo)


def get_data_updated_2025(end_date = current_date):
    files = glob(INDEXES_DIR + "/*")  # Get all CSV files in the directory

    # Generate full date range from 1980 to 2025
    dates = pd.date_range(start="1975-01", end=end_date, freq="MS").strftime("%m/%Y").to_numpy()
    df = pd.DataFrame({'Date': dates})  # Initialize DataFrame with all dates

    cols = ['Date']

    # Read and merge all CSV files
    for file in files:
        df_ = pd.read_csv(file)
        df = pd.merge(df, df_, how='left')  # Use left join to keep all dates
        cols.append(df_.columns[-1])

    # Keep only the required columns
    df = df[cols]

    # Save the final dataset
    df.to_csv('data/Historical_data_updated.csv', index=False)
    return df