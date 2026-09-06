import pandas as pd
from sqlalchemy import create_engine

# Database credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = "109080"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "olist_ecommerce"

# Read the validated dataset
csv_path = "data/processed/ecommerce_analysis_ready.csv"
print("Reading CSV...")
df = pd.read_csv(csv_path)

# Connect and upload
connection_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_url)

print("Uploading to MySQL table 'ecommerce_analysis_ready'...")
df.to_sql(
    name="ecommerce_analysis_ready",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("SUCCESS: Data successfully uploaded to MySQL!")