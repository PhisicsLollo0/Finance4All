
from datetime import datetime
import pandas as pd
from glob import glob

def get_data_info():
    """
    This function returns the first and last date available for each index.
    It also returns the name of the index.
    """
    available_indexes = glob("data/indexes/*.csv")

    index_name         = []
    last_date_available = []
    first_date_available = []

    for i in range(len(available_indexes)):
        df = pd.read_csv(available_indexes[i])
        last_date_available.append(df.Date.values[-1])
        first_date_available.append(df.Date.values[0])
        index_name.append(df.columns[-1])

    index_dictionary = pd.DataFrame({
        "index_name": index_name,
        "first_date_available": first_date_available,
        "last_date_available": last_date_available,
    })

    return index_dictionary