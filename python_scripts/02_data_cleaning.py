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

DATA_DIR = os.path.join(BASE_DIR, "data")

CLEANED_DATA_DIR = os.path.join(
    DATA_DIR,
    "cleaned"
)

# Create cleaned folder if it doesn't exist
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)


# ==========================================
# LOAD DATASETS
# ==========================================

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
    os.path.join(
        DATA_DIR,
        "product_category_name_translation.csv"
    )
)


# ==========================================
# 1. GEOLOCATION CLEANING
# ==========================================

print("Cleaning Geolocation Dataset...")

geolocation = geolocation.drop_duplicates()

print("Remaining rows:", geolocation.shape[0])


# ==========================================
# 2. ORDER REVIEWS CLEANING
# ==========================================

print("\nCleaning Order Reviews Dataset...")

# Missing review comments are normal because
# customers may give only a rating

order_reviews["review_comment_title"] = (
    order_reviews["review_comment_title"].fillna("No Title")
)

order_reviews["review_comment_message"] = (
    order_reviews["review_comment_message"].fillna("No Comment")
)


# Convert date columns

order_reviews["review_creation_date"] = pd.to_datetime(
    order_reviews["review_creation_date"]
)

order_reviews["review_answer_timestamp"] = pd.to_datetime(
    order_reviews["review_answer_timestamp"]
)


# ==========================================
# 3. ORDERS CLEANING
# ==========================================

print("\nCleaning Orders Dataset...")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column]
    )


# ==========================================
# 4. ORDER ITEMS CLEANING
# ==========================================

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"]
)


# ==========================================
# 5. PRODUCTS CLEANING
# ==========================================

print("\nCleaning Products Dataset...")

# Replace missing category with Unknown

products["product_category_name"] = (
    products["product_category_name"]
    .fillna("unknown")
)

# Fill numerical missing values with median

numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:

    products[column] = products[column].fillna(
        products[column].median()
    )


# ==========================================
# SAVE CLEANED DATASETS
# ==========================================

print("\nSaving cleaned datasets...")

customers.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "customers_cleaned.csv"
    ),
    index=False
)

geolocation.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "geolocation_cleaned.csv"
    ),
    index=False
)

order_items.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "order_items_cleaned.csv"
    ),
    index=False
)

order_payments.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "order_payments_cleaned.csv"
    ),
    index=False
)

order_reviews.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "order_reviews_cleaned.csv"
    ),
    index=False
)

orders.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "orders_cleaned.csv"
    ),
    index=False
)

products.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "products_cleaned.csv"
    ),
    index=False
)

sellers.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "sellers_cleaned.csv"
    ),
    index=False
)

category_translation.to_csv(
    os.path.join(
        CLEANED_DATA_DIR,
        "category_translation_cleaned.csv"
    ),
    index=False
)


print("\n" + "=" * 50)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 50)

print(f"\nCleaned files saved in:\n{CLEANED_DATA_DIR}")