import requests,csv,json,logging,gzip,io,datetime
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
        "api_key" : config.get("daily_api","api_key"),
        "database":config.get("postgres","database"),
        "table":config.get("postgres",'table')
    }

def fetch_historical_data(station_number,settings:dict) :
    """
    Ingests data from Meteostat API in csv.gz and save them into database

    :param station_number: Number of region station.
    :param settings: settings dictionary.
    :return: None.
    """
    header = {'x-api-key':settings["api_key"]}
    today = datetime.date.today()
    yestarday = today - datetime.timedelta(days=1)
    url = "https://api.meteostat.net/v2/stations/daily?station={}&start={}&end={}".format(station_number,yestarday,yestarday)
    data = requests.get(url, headers=header)
    if data.status_code == 200 and data.json()["data"] != None:
        df = pd.DataFrame(data.json()["data"])
        df = df.rename(columns={   # Renaming All Columns to fit SQL Table
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
        df= df.fillna(0) # Converting NAN to 0
        df["year"] = pd.DatetimeIndex(df["date"]).year
        df["month"] = pd.DatetimeIndex(df["date"]).month
        return df



if __name__ == '__main__':
    settings = load_settings()
    station_number = 10382 # if we want to change station we only have to change station number
    df_weather = fetch_historical_data(station_number,settings)
    try:
        if len(df_weather.columns) > 0:
            conn = db_sets.connect() # Connect to database
            db_sets.create_table(conn,settings["create_script"]) # Create table if not exists
            db_sets.execute_values(conn,df_weather,settings["table"]) # Bulk insert data into Table
    except Exception as e:
        logging.info("No data retrieved to update db!")

