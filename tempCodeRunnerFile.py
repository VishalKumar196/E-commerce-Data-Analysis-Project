# =========================================
# Brazilian E-Commerce Data Analysis
# ZIP SAFE VERSION (FINAL)
# =========================================

import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile

DATA_PATH = "Data"

# -----------------------------
# STEP 1: UNZIP ALL FILES
# -----------------------------
for file in os.listdir(DATA_PATH):
    if file.endswith(".zip"):
        zip_path = os.path.join(DATA_PATH, file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_PATH)
        print(f"Extracted: {file}")

print("\nFiles after extraction:")
print(os.listdir(DATA_PATH))

# -----------------------------
# STEP 2: AUTO-DETECT CSV FILES
# -----------------------------
files = os.listdir(DATA_PATH)

orders_file = [f for f in files if "orders_dataset" in f and f.endswith(".csv")][0]
items_file = [f for f in files if "order_items_dataset" in f and f.endswith(".csv")][0]
products_file = [f for f in files if "products_dataset" in f and f.endswith(".csv")][0]
customers_file = [f for f in files if "customers_dataset" in f and f.endswith(".csv")][0]

print("\nDetected CSV Files:")
print(orders_file)
print(items_file)
print(products_file)
print(customers_file)

# -----------------------------
# STEP 3: LOAD DATASETS
# -----------------------------
orders = pd.read_csv(os.path.join(DATA_PATH, orders_file))
items = pd.read_csv(os.path.join(DATA_PATH, items_file))
products = pd.read_csv(os.path.join(DATA_PATH, products_file))
customers = pd.read_csv(os.path.join(DATA_PATH, customers_file))

print("\nDataset Shapes:")
print("Orders:", orders.shape)
print("Items:", items.shape)
print("Products:", products.shape)
print("Customers:", customers.shape)

# -----------------------------
# STEP 4: MERGE DATA
# -----------------------------
df = orders.merge(items, on="order_id")
df = df.merge(products, on="product_id")
df = df.merge(customers, on="customer_id")

print("\nMerged Dataset Shape:", df.shape)
print(df.head())

# -----------------------------
# STEP 5: CLEANING
# -----------------------------
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df = df[df["order_status"] == "delivered"]

# -----------------------------
# STEP 6: SALES METRIC
# -----------------------------
df["sales"] = df["price"] + df["freight_value"]

# -----------------------------
# STEP 7: BUSINESS INSIGHTS
# -----------------------------
print("\nTotal Revenue:", round(df["sales"].sum(), 2))

df["month"] = df["order_purchase_timestamp"].dt.month
monthly_sales = df.groupby("month")["sales"].sum()

top_categories = (
    df.groupby("product_category_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_states = (
    df.groupby("customer_state")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nMonthly Sales:")
print(monthly_sales)

print("\nTop 10 Categories:")
print(top_categories)

print("\nTop 10 States:")
print(top_states)

# -----------------------------
# STEP 8: VISUALIZATION
# -----------------------------
plt.figure()
monthly_sales.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()

# =========================================
# END
# =========================================