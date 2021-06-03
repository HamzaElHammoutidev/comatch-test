#!/bin/bash

echo "Fetching Historical Data..."
python ./historical_data.py
echo "Historical Data Fetched!"
echo "Fetching Daily Data..."
python ./daily_data.py
echo "Daily Data fetched!"
echo "Average Air Temparature in Berlin"
python ./analytics.py
