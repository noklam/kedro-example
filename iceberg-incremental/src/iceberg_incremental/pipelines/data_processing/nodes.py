"""
This is a boilerplate pipeline 'load_dates'
generated using Kedro 0.19.8
"""

import pandas as pd
from datetime import datetime, timedelta
import clickhouse_connect
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

host = "clickpy-clickhouse.clickhouse.com"
username = "play"
database = "pypi"
secure = True
port = 443


def filter_pypi_data_clickhouse(table, start_date, end_date):
    """Load data for all dates between start_date and end_date and append into a single DataFrame."""
    logger.info(f"Starting data load from {start_date} to {end_date}.")
    query = (
        table.filter(table.project.like("%kedro%"))
        .filter(table.date <= end_date)
        .filter(table.date >= start_date)  # Limit results to 5 rows
    )
    data = query.to_pandas()
    logger.info(f"Total number of rows after loading: {data.shape[0]}")

    return data

