import requests,csv,json,logging,gzip,io
from configparser import ConfigParser
from urllib.request import urlopen
import pandas as pd
import db_sets


logging.basicConfig(level = logging.INFO)

def load_settings() -> dict:
    """
    Loads settings from files

    :return: dictionary with settings key-value pairs.
    """

    config = ConfigParser()
    config.read("settings.ini")

    return {
        "create_script" : config.get("postgres","creation_table"),
        "database":config.get("postgres","database"),
        "table":config.get("postgres",'table')
    }

def fetch_historical_data(station_number) :
    """
    Ingests data from Meteostat API in csv.gz and save them into database

    :param station_number: Number of region station.
    :return: None.
    """
    api = "https://bulk.meteostat.net/v2/daily/full/{}.csv.gz".format(str(station_number))
    csv_data = pd.read_csv(api, compression='gzip',
                   error_bad_lines=False,header=None)
    csv_data = csv_data.rename(columns={   # Renaming All Columns to fit SQL Table
        0:"date",
        1:"tavg",
        2:"tmin",
        3:"tmax",
        4:"prcp",
        5:"snow",
        6:"wdir",
        7:"wspd",
        8:"wpgt",
        9:"pres",
        10:"tsun",

    })
    csv_data= csv_data.fillna(0) # Converting NAN to 0
    csv_data["year"] = pd.DatetimeIndex(csv_data["date"]).year
    csv_data["month"] = pd.DatetimeIndex(csv_data["date"]).month
    return csv_data

def query_check(conn):
    """
    Checks if Database contains data.

    :param conn: Database Connection.
    :return: Historical Data Count.
    """
    query = "SELECT COUNT(*) FROM weather "
    db_sets.create_table(conn,settings["create_script"]) # Create table if not exists
    count = db_sets.analytics_query(conn,query)
    logging.info("Database contains {} rows!".format(str(count)))


if __name__ == '__main__':
    settings = load_settings()
    station_number = 10382 # if we want to change station we only have to change station number
    df_weather = fetch_historical_data(station_number)
    conn = db_sets.connect() # Connect to database
    db_sets.create_table(conn,settings["create_script"]) # Create table if not exists
    db_sets.execute_values(conn,df_weather,settings["table"]) # Bulk insert data into Table
    query_check(conn)
