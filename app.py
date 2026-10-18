# Superstore Sales Analysis - Streamlit App
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration

st.set_page_config(
page_title="Superstore Sales Analysis",
page_icon="📊",
layout="wide"
)

# Dashboard title

st.title("📊 Superstore Sales Analysis")
st.write("Explore sales, profit, products, and regional performance.")

# Load dataset

@st.cache_data
def load_data():
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
return df

try:
df = load_data()

```
# Sidebar filters
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

filtered_df = df[
    df["Region"].isin(regions) &
    df["Category"].isin(categories)
]

# Key performance indicators
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Orders", f"{filtered_df['Order ID'].nunique():,}")
col4.metric("Units Sold", f"{filtered_df['Quantity'].sum():,}")

st.divider()

# Sales by category
st.subheader("Sales by Category")
category_sales = (
    filtered_df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig1 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Total Sales by Product Category"
)
st.plotly_chart(fig1, use_container_width=True)

# Sales over time
st.subheader("Monthly Sales Trend")
monthly_sales = (
    filtered_df.set_index("Order Date")["Sales"]
    .resample("MS")
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Over Time"
)
st.plotly_chart(fig2, use_container_width=True)

# Profit by region
st.subheader("Profit by Region")
region_profit = (
    filtered_df.groupby("Region", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig3 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Profit",
    title="Total Profit by Region"
)
st.plotly_chart(fig3, use_container_width=True)

# Top products
st.subheader("Top 10 Products by Sales")
top_products = (
    filtered_df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .nlargest(10, "Sales")
    .sort_values("Sales", ascending=True)
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products"
)
st.plotly_chart(fig4, use_container_width=True)

# Data preview
with st.expander("View Dataset"):
    st.dataframe(filtered_df.head(100), use_container_width=True)
```

except FileNotFoundError:
st.error(
"Dataset not found. Please ensure 'Sample - Superstore.csv' "
"is uploaded to the same folder as app.py in your GitHub repository."
)
except Exception as e:
st.error(f"Something went wrong while loading the dataset: {e}")
