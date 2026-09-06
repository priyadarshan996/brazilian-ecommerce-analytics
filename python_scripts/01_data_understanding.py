import pandas as pd
import os

# -------------------------------
# Project and data folder paths
# -------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(BASE_DIR, "data")


# -------------------------------
# Load datasets
# -------------------------------

customers = pd.read_csv(
    os.path.join(DATA_DIR, "olist_customers_dataset.csv")
)

geolocation = pd.read_csv(
    os.path.join(DATA_DIR, "olist_geolocation_dataset.csv")
)

order_items = pd.read_csv(
    os.path.join(DATA_DIR, "olist_order_items_dataset.csv")
)

order_payments = pd.read_csv(
    os.path.join(DATA_DIR, "olist_order_payments_dataset.csv")
)

order_reviews = pd.read_csv(
    os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv")
)

orders = pd.read_csv(
    os.path.join(DATA_DIR, "olist_orders_dataset.csv")
)

products = pd.read_csv(
    os.path.join(DATA_DIR, "olist_products_dataset.csv")
)

sellers = pd.read_csv(
    os.path.join(DATA_DIR, "olist_sellers_dataset.csv")
)

category_translation = pd.read_csv(
    os.path.join(DATA_DIR, "product_category_name_translation.csv")
)


# -------------------------------
# Store datasets
# -------------------------------

datasets = {
    "Customers": customers,
    "Geolocation": geolocation,
    "Order Items": order_items,
    "Order Payments": order_payments,
    "Order Reviews": order_reviews,
    "Orders": orders,
    "Products": products,
    "Sellers": sellers,
    "Category Translation": category_translation
}


# -------------------------------
# Dataset overview
# -------------------------------

for name, df in datasets.items():

    print("\n" + "=" * 50)
    print(f"{name.upper()} DATASET")
    print("=" * 50)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 Rows:")
    print(df.head())