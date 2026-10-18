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
st.title("📊 Superstore Sales & Business Performance Analysis")
st.markdown("Explore sales drivers, profitability bottlenecks, and regional performance trends.")

# ----------------------------------
# 3. Load Dataset
# ----------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Ship Date"] = pd.to_datetime(data["Ship Date"])
    return data

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
    default=region_options,
    key="filter_region"
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=category_options,
    default=category_options,
    key="filter_category"
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
# 6. Sales & Profit by Category
# ----------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Sales by Product Category")
    category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s"
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col_b:
    st.subheader("Profit by Product Category")
    category_profit = filtered_df.groupby("Category")["Profit"].sum().reset_index()
    fig_profit = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        color="Profit",
        color_continuous_scale="RdYlGn",
        text_auto=".2s"
    )
    st.plotly_chart(fig_profit, use_container_width=True)

st.divider()

# ----------------------------------
# 7. Deep Dive: Sub-Category Profitability
# ----------------------------------
st.subheader("🔍 Sub-Category Profitability Analysis")
st.markdown("Identify which specific sub-categories are driving profits versus those causing losses.")

subcat_profit = filtered_df.groupby(["Sub-Category", "Category"])["Profit"].sum().reset_index()
subcat_profit = subcat_profit.sort_values(by="Profit", ascending=True)

fig_subcat = px.bar(
    subcat_profit,
    x="Profit",
    y="Sub-Category",
    color="Profit",
    orientation="h",
    color_continuous_scale="RdYlGn",
    title="Profit/Loss by Sub-Category"
)
st.plotly_chart(fig_subcat, use_container_width=True)

st.divider()

# ----------------------------------
# 8. Monthly Sales Trend Over Time
# ----------------------------------
st.subheader("📈 Monthly Sales Trend")

trend_df = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
trend_df["Order Date"] = trend_df["Order Date"].dt.to_timestamp()

fig_trend = px.line(
    trend_df,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Sales Performance Over Time"
)
st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ----------------------------------
# 9. Raw Data Table & Download
# ----------------------------------
with st.expander("📂 View & Download Filtered Dataset"):
    st.dataframe(filtered_df)
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name='filtered_superstore_data.csv',
        mime='text/csv',
    )
