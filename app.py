import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="Superstore Sales Analysis",
page_icon="📊",
layout="wide"
)

st.title("📊 Superstore Sales Analysis")
st.write("Explore sales, profit, products, and regional performance.")

@st.cache_data
def load_data():
df =    pd.read_csv("Sample - Superstore.csv", encoding="latin1")
df["Order Date"] =    pd.to_datetime(df["Order Date"])
df["Ship Date"] =    pd.to_datetime(df["Ship Date"])
return df

try:
df = load_data()

```
st.sidebar.header("Filters")

all_regions = sorted(df["Region"].dropna().unique().tolist())
all_categories = sorted(df["Category"].dropna().unique().tolist())

regions = st.sidebar.multiselect(
    "Select Region",
    options=all_regions,
    default=all_regions
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=all_categories,
    default=all_categories
)

filtered_df = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
]

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Orders", f"{filtered_df['Order ID'].nunique():,}")
col4.metric("Units Sold", f"{filtered_df['Quantity'].sum():,}")

st.divider()

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
    title="Total Sales by Product Category",
    color="Category"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(
        pd.Grouper(key="Order Date", freq="MS")
    )["Sales"]
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
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig4, use_container_width=True)

with st.expander("View Dataset"):
    st.dataframe(filtered_df.head(100), use_container_width=True)
```

except FileNotFoundError:
st.error(
"Dataset not found. Check that 'Sample - Superstore.csv' "
"is in the same GitHub folder as app.py."
)

except Exception as e:
st.error(f"An error occurred: {e}")
