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

PROCESSED_DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


# ==========================================
# LOAD MASTER DATASET
# ==========================================

master_data = pd.read_csv(
    os.path.join(
        PROCESSED_DATA_DIR,
        "ecommerce_master.csv"
    )
)


# ==========================================
# 1. CHECK ORDER STATUS
# ==========================================

print("\n" + "=" * 60)
print("ORDER STATUS DISTRIBUTION")
print("=" * 60)

print(
    master_data["order_status"]
    .value_counts()
)


# ==========================================
# 2. REMOVE ORDERS WITHOUT ITEMS
# ==========================================

print("\n" + "=" * 60)
print("REMOVING ORDERS WITHOUT ITEMS")
print("=" * 60)

print("Before:", master_data.shape)

analysis_data = master_data.dropna(
    subset=["product_id"]
).copy()

print("After:", analysis_data.shape)


# ==========================================
# 3. HANDLE MISSING CATEGORY TRANSLATION
# ==========================================

analysis_data["product_category_name_english"] = (
    analysis_data["product_category_name_english"]
    .fillna("unknown")
)


# ==========================================
# 4. PAYMENT VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("MISSING PAYMENT RECORDS")
print("=" * 60)

print(
    analysis_data[
        analysis_data["total_payment"].isnull()
    ][
        ["order_id", "order_status"]
    ]
)


# ==========================================
# 5. REVIEW SCORE VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("MISSING REVIEW SCORES")
print("=" * 60)

print(
    "Missing review scores:",
    analysis_data["review_score"].isnull().sum()
)


# ==========================================
# 6. DELIVERY DATA VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("DELIVERY DAYS SUMMARY")
print("=" * 60)

print(
    analysis_data["delivery_days"]
    .describe()
)


# Check negative delivery days

negative_delivery = analysis_data[
    analysis_data["delivery_days"] < 0
]

print("\nNegative delivery records:")
print(len(negative_delivery))


# ==========================================
# 7. FINAL DATASET CHECK
# ==========================================

print("\n" + "=" * 60)
print("FINAL DATASET INFORMATION")
print("=" * 60)

print("\nShape:")
print(analysis_data.shape)

print("\nMissing Values:")
print(analysis_data.isnull().sum())


# ==========================================
# SAVE ANALYSIS-READY DATASET
# ==========================================

analysis_data.to_csv(
    os.path.join(
        PROCESSED_DATA_DIR,
        "ecommerce_analysis_ready.csv"
    ),
    index=False
)


print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED SUCCESSFULLY!")
print("=" * 60)