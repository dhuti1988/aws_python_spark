# This code will generate a data file in S3 with format: channel_id, customer_id, transaction_id, transaction_date, amount, merchant_name
# The data file will be named as data_<timestamp>.csv
# Data will be generated for 10 rows
# channel will be one of ["phone", "web", "app"]
# customer_id will start with 1 and have 5 digits
# transaction_id will be a uuid
# transaction_date is any date YYYY-MM-DD between 2025-01-01 and 2026-12-31
# amount will be a random number between 1 and 1000
# merchant_name will be a random name from ["amazon", "ebay", "walmart", "target", "best buy", "costco", "aldi"]

import random
import uuid
from datetime import datetime

import boto3
import pandas as pd

CHANNELS = ["phone", "web", "app"]
MERCHANTS = ["amazon", "ebay", "walmart", "target", "best buy", "costco", "aldi"]


def generate_dataframe():
    rows = []
    for _ in range(10):
        year = random.randint(2025, 2026)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        transaction_date = f"{year}-{month:02d}-{day:02d}"
        rows.append({
            "channel_id": random.choice(CHANNELS),
            "customer_id": str(random.randint(10000, 99999)),
            "transaction_id": str(uuid.uuid4()),
            "transaction_date": transaction_date,
            "amount": random.randint(1, 1000),
            "merchant_name": random.choice(MERCHANTS),
        })
    return pd.DataFrame(rows)


def main():
    s3_bucket = "ad-demo-bucket-205930608840"
    s3_prefix = "customer_data"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    part_key = timestamp[:8]
    file_name_key = timestamp[8:]
    s3_path = f"s3://{s3_bucket}/{s3_prefix}/{part_key}/customer_transactions_{file_name_key}.csv"

    df = generate_dataframe()
    df.to_csv(s3_path, index=False)
    return s3_path


if __name__ == "__main__":  
    s3_path = main()
    print(f"Data saved to {s3_path}")