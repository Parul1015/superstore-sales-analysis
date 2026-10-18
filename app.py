import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# 1. Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Superstore Sales Analysis",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------
# 2. Dashboard Title
# ----------------------------------
st.title("📊 Superstore Sales Analysis")
st.markdown("Explore sales, profit, product categories, and regional performance.")

# ----------------------------------
# 3. Load Dataset
# ----------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Ship Date"] = pd.to_datetime(data["Ship Date"])
    return data  # Fixed indentation here

df = load_data()

# ----------------------------------
# 4. Sidebar Filters
# ----------------------------------
st.sidebar.header("Dashboard Filters")

region_options = sorted(df["Region"].dropna().unique())
category_options = sorted(df["Category"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=region_options,
    default=region_options
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=category_options,
    default=category_options
)

filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
]

# ----------------------------------
# 5. Key Performance Indicators
# ----------------------------------
st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Units Sold", f"{total_quantity:,}")

st.divider()

# ----------------------------------
# 6. Sales by Category
# ----------------------------------
st.subheader("Sales by Product Category")

category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=".2s",
    title="Total Sales by Product Category"
)
st.plotly_chart(fig_category, use_container_width=True)

#Monthly Sales Trend Line Chart
st.subheader("Sales Trend Over Time")

sales_trend = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
sales_trend["Order Date"] = sales_trend["Order Date"].dt.to_timestamp()

fig_trend = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

st.subheader("Profitability by Region")

#Regional Profitability Map or Chart
region_profit = filtered_df.groupby("Region")["Profit"].sum().reset_index()

fig_region = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Profit",
    color_continuous_scale="RdYlGn",
    title="Total Profit by Region"
)
st.plotly_chart(fig_region, use_container_width=True)

#Allow Raw Data Download
with st.expander("View & Download Raw Filtered Data"):
    st.dataframe(filtered_df)
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name='filtered_superstore_data.csv',
        mime='text/csv',
    )
st.plotly_chart(fig_trend, use_container_width=True)
