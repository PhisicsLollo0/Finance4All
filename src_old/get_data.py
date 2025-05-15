import pandas as pd

import json
import requests
import urllib.parse

from glob import glob



def generate_csv():
        
    if len(glob('*.csv')) == 0:

    
        response = requests.get("https://api.github.com/repos/NandayDev/MSCI-Historical-Data/git/trees/main?recursive=1")
        json_response = json.loads(response.text)
        dfs=[]
        for branch in json_response["tree"]:
            if ("countries" in branch["path"] or "indexes" in branch["path"] ) and "csv" in branch["path"]:
                filename = "https://raw.githubusercontent.com/NandayDev/MSCI-Historical-Data/main/" + urllib.parse.quote(branch["path"])
                print(filename)
                dfs.append(pd.read_csv(filename,index_col=0,skiprows=1,header=0,names=["Date",filename[filename.rfind("/")+1:-4].replace("%20"," ")]))
        for branch in json_response["tree"]:
            if ("curvo" in branch["path"] ) and "csv" in branch["path"]: # in modo da averli DOPO e quindi in caso di duplicati scartare QUESTI e non i precedenti
                filename = "https://raw.githubusercontent.com/NandayDev/MSCI-Historical-Data/main/" + urllib.parse.quote(branch["path"])
                print(filename)
                dfs.append(pd.read_csv(filename,index_col=0,skiprows=1,header=0,names=["Date",filename[filename.rfind("/")+1:-4].replace("%20"," ")]))

        data = pd.concat(dfs,axis=1).sort_values(by="Date")
        data = data.iloc[:,~data.columns.duplicated()] #remove duplicates

        # ATTENZIONE SISTEMIAMO RUSSIA VALUE e RUSSIA GROWTH
        data.loc["2022-03":,"MSCI RUSSIA VALUE"].fillna(0.001, inplace=True)
        data.loc["2022-03":,"MSCI RUSSIA GROWTH"].fillna(0.001, inplace=True)

        data.fillna(method="ffill",limit=6,inplace=True)

        data.to_csv('Historical_data.csv')

    else:
        print("Data already present")


def prune_csv():
    
    data = pd.read_csv('Historical_data.csv')

    columns = ['Date', 
               'S%26P 500',
               'S%26P 500 Minimum Volatility',
               'MSCI ACWI',
               'MSCI WORLD',
               'MSCI World',
               'MSCI Europe',
               'MSCI Emerging Markets',
               'MSCI USA Small Cap Value Weighted',
               'MSCI Europe Small Cap Value Weighted',
               'FTSE World Government Bond Developed Markets',
               'FTSE World Government Bond G7',
               'Gold spot',
               ]
    
    renamed_columns = {
                        'S%26P 500' : 'S&P 500',
                        'S%26P 500 Minimum Volatility' : 'S&P 500 Minimum Volatility'
                        }

    data_pruned = data[columns]
    data_pruned = data_pruned.rename(columns=renamed_columns)

    data_pruned.to_csv('Historical_data_pruned.csv')



def get_data_updated_2025(end_date = "2025-04"):
    files = glob('/home/cavallo/Finance/src/data_updated_2025/*')

    # Generate full date range from 1980 to 2025
    dates = pd.date_range(start="1975-01", end=end_date, freq="MS").strftime("%m/%Y").to_numpy()
    df = pd.DataFrame({'Date': dates})  # Initialize DataFrame with all dates

    # Read and merge all CSV files
    for file in files:
        df_ = pd.read_csv(file)
        df = pd.merge(df, df_, how='left')  # Use left join to keep all dates

    # Define columns to keep
    cols = ['Date',
            'S&P 500',
            'S&P 500 Minimum Volatility',
            'MSCI ACWI',
            'MSCI World',
            'MSCI Europe',
            'MSCI Emerging Markets',
            'MSCI USA Small Cap Value Weighted',
            'MSCI Europe Small Cap Value Weighted',
            'FTSE World Government Bond - Developed Markets']

    # Keep only the required columns
    df = df[cols]

    # Save the final dataset
    df.to_csv('Historical_data_updated_2025.csv', index=False)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

DOWNLOAD_DIR = "/home/cavallo/Finance/src/data_updated_2025"

def download_from_curvo(file_name, url_curvo):

    # Set up options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.prompt_for_download": False,
        "download.default_directory": DOWNLOAD_DIR,  # Change this to your download folder
        "profile.default_content_settings.popups": 0,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Launch browser
    driver = webdriver.Chrome(options=chrome_options)

    # Go to the page
    driver.get(url_curvo)

    wait = WebDriverWait(driver, 20)
    export_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chart-button-export-as-csv")))

    # Step 3: Click the export button
    export_button.click()

    original_filename = "chart.csv"  # <-- this is the default downloaded name
    new_filename = file_name  # <-- whatever you want

    # Build full paths
    original_path = os.path.join(DOWNLOAD_DIR, original_filename)
    new_path = os.path.join(DOWNLOAD_DIR, new_filename)

    # Wait for the file to exist (extra safe)
    for _ in range(10):
        if os.path.exists(original_path):
            break
        time.sleep(1)

    # Rename
    if os.path.exists(original_path):
        os.rename(original_path, new_path)
        print(f"File downloaded and renamed to {new_path}")
    else:
        print("Download failed or file not found.")

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
                            ]

    for i in range(len(dict_indexes_on_curvo)):
        download_from_curvo(*dict_indexes_on_curvo[i])