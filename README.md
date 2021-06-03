# COMATCH TEST CODE

As the test leaves the choice of assumptions and technologies, I have decided to go with Python and PostgresSQL

## Deploy & Run

Use docker compose :

```bash
docker-compose up --build 
```

## Project Structure

```
root/
|-- db/
|   |-- create_table.sql
|   |-- Dockerfile
|-- analytics.py
|-- daily_data.py
|-- db_sets.py
|-- historical_data.py
|-- Dockerfile
|-- requirements.txt
|-- script_wrapper.sh
|-- settings.ini
```

## Project Structure Details

- create_table.sql :
  - Create Database
  - Grant Privileges
  - Create Daily Weather Data Table
- Dockerfile (db) :
  - Associated to run PostgresSQL container
- Analytics.py :
  - Perform anlytics on DB ( Average Air Temperature )
- daily_data.py :
  - Gets back daily recent data from Meteostat API
- db_sets.py :
  - Contains database setup and all pre-made helping functions
- historical_data.py :
  - Gets back all historical data daily from Meteostat API
- Dockerfile (root) :
  - Associated to Python script to run python data container
- requiremets.txt :
  - Required Packages to install file
- script_wrapper.sh :
  - To run all python scripts
- settings.ini :
  - contains diffrent required configuration

## Reasoning

- Historical Data :

  - To fetch historical data I consumed Bulk Daily Data API provieded by Meteostat, that provides daily weather data starting from 1936-06-12 to 2021-06-11
  - Transformed data to split provided string data into two different columns which are (year and month)
  - Used date columns as Primary key, because I don't want duplicates on my database, since data is provided daily, each and every row represents a day
  - Inserted all historical in a single query (execute_values:db_sets), I had a lot of choices over functions proposed by psycopg2, but execute_values on extras is the most perfoming one for my case
- Daily Data :

  - To fetch daily data consumed JSON API Meteostat, that prvovides daily weather data for a range of 370 days, between a specified start and end date, that for my case precised in previous day only, because we are fetching data daily
  - Used date columns as Primary key, because I don't want duplicates on my database, since data is provided daily, each and every row represents a day
  - Checked if there  is any data, if not I log no updates, otherwise I use simple insert query, since we'll alaways have a single row to add because it is a daily range
- Analytics :

  - It was easy for me to fetch average air temparture since I splited date column on fetching from API with Pandas
