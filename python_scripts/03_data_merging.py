import pandas as pd
import os


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CLEANED_DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

PROCESSED_DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


# ==========================================
# LOAD CLEANED DATASETS
# ==========================================

customers = pd.read_csv(
    os.path.join(CLEANED_DATA_DIR, "customers_cleaned.csv")
)

orders = pd.read_csv(
    os.path.join(CLEANED_DATA_DIR, "orders_cleaned.csv")
)

order_items = pd.read_csv(
    os.path.join(CLEANED_DATA_DIR, "order_items_cleaned.csv")
)

products = pd.read_csv(
    os.path.join(CLEANED_DATA_DIR, "products_cleaned.csv")
)

category_translation = pd.read_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "category_translation_cleaned.csv"
    )
)

order_payments = pd.read_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "order_payments_cleaned.csv"
    )
)

order_reviews = pd.read_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "order_reviews_cleaned.csv"
    )
)


# ==========================================
# 1. AGGREGATE PAYMENTS
# ==========================================

payments_agg = (
    order_payments
    .groupby("order_id")
    .agg(
        total_payment=("payment_value", "sum"),
        total_installments=("payment_installments", "max")
    )
    .reset_index()
)


# ==========================================
# 2. AGGREGATE REVIEWS
# ==========================================

reviews_agg = (
    order_reviews
    .groupby("order_id")
    .agg(
        review_score=("review_score", "mean")
    )
    .reset_index()
)


# ==========================================
# 3. MERGE ORDERS + CUSTOMERS
# ==========================================

master_data = orders.merge(
    customers,
    on="customer_id",
    how="left"
)


# ==========================================
# 4. MERGE ORDER ITEMS
# ==========================================

master_data = master_data.merge(
    order_items,
    on="order_id",
    how="left"
)


# ==========================================
# 5. MERGE PRODUCTS
# ==========================================

master_data = master_data.merge(
    products,
    on="product_id",
    how="left"
)


# ==========================================
# 6. MERGE CATEGORY TRANSLATION
# ==========================================

master_data = master_data.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


# ==========================================
# 7. MERGE PAYMENTS
# ==========================================

master_data = master_data.merge(
    payments_agg,
    on="order_id",
    how="left"
)


# ==========================================
# 8. MERGE REVIEWS
# ==========================================

master_data = master_data.merge(
    reviews_agg,
    on="order_id",
    how="left"
)


# ==========================================
# 9. CREATE USEFUL FEATURES
# ==========================================

master_data["total_item_value"] = (
    master_data["price"]
    + master_data["freight_value"]
)

master_data["purchase_month"] = pd.to_datetime(
    master_data["order_purchase_timestamp"]
).dt.to_period("M").astype(str)

master_data["purchase_year"] = pd.to_datetime(
    master_data["order_purchase_timestamp"]
).dt.year

master_data["purchase_day"] = pd.to_datetime(
    master_data["order_purchase_timestamp"]
).dt.day_name()


# Delivery time

master_data["order_delivered_customer_date"] = pd.to_datetime(
    master_data["order_delivered_customer_date"]
)

master_data["order_purchase_timestamp"] = pd.to_datetime(
    master_data["order_purchase_timestamp"]
)

master_data["delivery_days"] = (
    master_data["order_delivered_customer_date"]
    - master_data["order_purchase_timestamp"]
).dt.days


# ==========================================
# FINAL CHECK
# ==========================================

print("=" * 60)
print("MASTER DATASET CREATED")
print("=" * 60)

print("\nShape:", master_data.shape)

print("\nMissing Values:")
print(master_data.isnull().sum())

print("\nFirst 5 Rows:")
print(master_data.head())


# ==========================================
# SAVE MASTER DATASET
# ==========================================

master_data.to_csv(
    os.path.join(
        PROCESSED_DATA_DIR,
        "ecommerce_master.csv"
    ),
    index=False
)

print("\nMaster dataset saved successfully!")

print(
    os.path.join(
        PROCESSED_DATA_DIR,
        "ecommerce_master.csv"
    )
)