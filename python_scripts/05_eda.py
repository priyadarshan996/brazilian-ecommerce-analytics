import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

data = pd.read_csv("data/processed/ecommerce_master.csv")


# ============================================================
# 2. BASIC DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print("\nDataset Shape:")
print(data.shape)

print("\nColumns:")
print(data.columns.tolist())

print("\nDataset Info:")
data.info()

print("\nMissing Values:")
print(data.isnull().sum())

print("\nDuplicate Rows:")
print(data.duplicated().sum())

print("\nStatistical Summary:")
print(data.describe())


# ============================================================
# 3. CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date"
]

for col in date_columns:
    data[col] = pd.to_datetime(data[col])


# ============================================================
# 4. CREATE ORDER-LEVEL DATASET
# ============================================================

order_level = (
    data.groupby("order_id")
    .agg(
        customer_id=("customer_unique_id", "first"),
        order_status=("order_status", "first"),
        order_date=("order_purchase_timestamp", "first"),
        total_payment=("total_payment", "first"),
        customer_state=("customer_state", "first"),
        customer_city=("customer_city", "first"),
        review_score=("review_score", "first"),
        delivery_days=("delivery_days", "first")
    )
    .reset_index()
)


# ============================================================
# 5. OVERALL BUSINESS OVERVIEW
# ============================================================

print("\n" + "=" * 60)
print("OVERALL BUSINESS OVERVIEW")
print("=" * 60)

total_orders = order_level["order_id"].nunique()

total_customers = order_level["customer_id"].nunique()

total_revenue = order_level["total_payment"].sum()

average_order_value = order_level["total_payment"].mean()

print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Revenue:", round(total_revenue, 2))
print("Average Order Value:", round(average_order_value, 2))


# ============================================================
# 6. ORDER STATUS ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("ORDER STATUS ANALYSIS")
print("=" * 60)

order_status = order_level["order_status"].value_counts()

print(order_status)


# ============================================================
# 7. MONTHLY SALES AND ORDERS TREND
# ============================================================

print("\n" + "=" * 60)
print("MONTHLY SALES AND ORDERS TREND")
print("=" * 60)

order_level["month"] = (
    order_level["order_date"]
    .dt.to_period("M")
)

monthly_trend = (
    order_level.groupby("month")
    .agg(
        total_orders=("order_id", "count"),
        total_revenue=("total_payment", "sum")
    )
)

print(monthly_trend)


# ============================================================
# 8. TOP PRODUCT CATEGORIES BY REVENUE
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCT CATEGORIES BY REVENUE")
print("=" * 60)

category_revenue = (
    data.groupby("product_category_name_english")
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .sort_values(
        by="total_revenue",
        ascending=False
    )
)

print(category_revenue.head(10))


# ============================================================
# 9. TOP PRODUCT CATEGORIES BY ORDERS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCT CATEGORIES BY ORDERS")
print("=" * 60)

category_orders = (
    data.groupby("product_category_name_english")
    ["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print(category_orders.head(10))


# ============================================================
# 10. TOP STATES BY ORDERS
# ============================================================

print("\n" + "=" * 60)
print("TOP STATES BY ORDERS")
print("=" * 60)

state_orders = (
    order_level.groupby("customer_state")
    ["order_id"]
    .count()
    .sort_values(ascending=False)
)

print(state_orders.head(10))


# ============================================================
# 11. TOP STATES BY REVENUE
# ============================================================

print("\n" + "=" * 60)
print("TOP STATES BY REVENUE")
print("=" * 60)

state_revenue = (
    order_level.groupby("customer_state")
    ["total_payment"]
    .sum()
    .sort_values(ascending=False)
)

print(state_revenue.head(10))


# ============================================================
# 12. TOP CITIES BY ORDERS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 CITIES BY ORDERS")
print("=" * 60)

city_orders = (
    order_level.groupby("customer_city")
    ["order_id"]
    .count()
    .sort_values(ascending=False)
)

print(city_orders.head(10))


# ============================================================
# 13. REVIEW SCORE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVIEW SCORE ANALYSIS")
print("=" * 60)

review_distribution = (
    order_level["review_score"]
    .value_counts()
    .sort_index()
)

print(review_distribution)

print(
    "\nAverage Review Score:",
    round(order_level["review_score"].mean(), 2)
)


# ============================================================
# 14. DELIVERY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DELIVERY ANALYSIS")
print("=" * 60)

delivered_orders = order_level[
    order_level["order_status"] == "delivered"
].copy()

print(
    "Average Delivery Days:",
    round(delivered_orders["delivery_days"].mean(), 2)
)

print(
    "\nDelivery Days Summary:"
)

print(
    delivered_orders["delivery_days"]
    .describe()
)


# ============================================================
# 15. TOP SELLERS BY SALES
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 SELLERS BY SALES")
print("=" * 60)

seller_sales = (
    data.groupby("seller_id")
    .agg(
        total_sales=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .sort_values(
        by="total_sales",
        ascending=False
    )
)

print(seller_sales.head(10))


# ============================================================
# 16. VISUALIZATION - MONTHLY REVENUE
# ============================================================

monthly_trend["total_revenue"].plot(
    figsize=(12, 6),
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 17. VISUALIZATION - ORDER STATUS
# ============================================================

order_status.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 18. VISUALIZATION - TOP 10 PRODUCT CATEGORIES
# ============================================================

category_revenue.head(10).sort_values(
    by="total_revenue"
)["total_revenue"].plot(
    kind="barh",
    figsize=(10, 6)
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")

plt.tight_layout()

plt.show()


# ============================================================
# 19. VISUALIZATION - TOP 10 STATES
# ============================================================

state_revenue.head(10).sort_values().plot(
    kind="barh",
    figsize=(10, 6)
)

plt.title("Top 10 States by Revenue")
plt.xlabel("Revenue")
plt.ylabel("State")

plt.tight_layout()

plt.show()


# ============================================================
# 20. VISUALIZATION - REVIEW SCORE DISTRIBUTION
# ============================================================

review_distribution.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.show()


print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY!")
print("=" * 60)


print(len(data))
