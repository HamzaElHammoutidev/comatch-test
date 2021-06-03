from configparser import ConfigParser
import db_sets,logging

logging.basicConfig(level=logging.INFO)

def load_settings():
    """
    Loads settings from files

    :return: dictionary with settings key-value pairs.
    """

    config = ConfigParser()
    config.read("settings.ini")

    return {
        "create_script" : config.get("postgres","creation_table"),
        "api_key" : config.get("daily_api","api_key"),
        "database":config.get("postgres","database")

    }

def avg_air_temp(month):
    """
    Retrieve back average air temparture for a specific month of all years

    :param month: Month to fetch analytics for.
    :return: average air temparture.
    """
    query = "SELECT AVG(tavg) FROM weather WHERE month = {}".format(month)
    conn = db_sets.connect() # Connect to database
    db_sets.create_table(conn,settings["create_script"]) # Create table if not exists
    avg = db_sets.analytics_query(conn,query)
    return avg

if __name__ == '__main__':
    settings = load_settings()
    avg = avg_air_temp(2)
    print(avg)