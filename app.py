"""
Superstore Sales Analytics — an interactive Streamlit dashboard over the
public "Sample - Superstore" retail dataset (9,994 US orders, 2014-2017).

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

COLOR_SALES = "#2a78d6"
COLOR_PROFIT = "#eb6834"
COLOR_FURNITURE = "#2a78d6"
COLOR_OFFICE = "#eb6834"
COLOR_TECH = "#1baf7a"
COLOR_POS = "#2a78d6"
COLOR_NEG = "#e34948"

st.set_page_config(
    page_title="Superstore Sales Analytics",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("superstore.csv", encoding="latin1", parse_dates=["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df


df = load_data()

st.title("📊 Superstore Sales & Profit")
st.caption(
    "Interactive breakdown of orders, revenue and profitability across regions, "
    "categories and time. Data: the public *Sample - Superstore* dataset "
    "(2014-2017 US retail orders) — the standard dataset used to learn BI/analytics tools. "
    "Personal portfolio project, not real company data."
)


with st.sidebar:
    st.header("Filters")
    years = st.multiselect(
        "Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique())
    )
    regions = st.multiselect(
        "Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
    )
    categories = st.multiselect(
        "Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
    )
    segments = st.multiselect(
        "Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique())
    )
    if st.button("Reset filters"):
        st.rerun()

f = df[
    df["Year"].isin(years)
    & df["Region"].isin(regions)
    & df["Category"].isin(categories)
    & df["Segment"].isin(segments)
]

if f.empty:
    st.warning("No orders match this filter combination. Adjust the filters in the sidebar.")
    st.stop()

#kpi
total_sales = f["Sales"].sum()
total_profit = f["Profit"].sum()
margin = (total_profit / total_sales * 100) if total_sales else 0
orders = f["Order ID"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Orders", f"{orders:,}", help=f"{len(f):,} line items")

st.divider()

#  category mix
st.subheader("Sales mix by category")
mix = f.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
cat_colors = {"Furniture": COLOR_FURNITURE, "Office Supplies": COLOR_OFFICE, "Technology": COLOR_TECH}
fig_mix = px.bar(
    mix, x="Sales", y="Category", orientation="h", text="Sales",
    color="Category", color_discrete_map=cat_colors,
)
fig_mix.update_traces(texttemplate="$%{text:,.0f}", textposition="outside", cliponaxis=False)
fig_mix.update_layout(
    showlegend=False, height=220, margin=dict(l=0, r=40, t=10, b=10),
    xaxis_title=None, yaxis_title=None, template="plotly_white",
)
st.plotly_chart(fig_mix, use_container_width=True)

#  trend + region 
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Monthly sales trend")
    trend = f.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month")
    fig_trend = px.area(trend, x="Month", y="Sales")
    fig_trend.update_traces(line_color=COLOR_SALES, fillcolor="rgba(42,120,214,0.15)")
    fig_trend.update_layout(
        height=340, margin=dict(l=0, r=10, t=10, b=10),
        yaxis_title=None, xaxis_title=None, template="plotly_white",
        yaxis_tickprefix="$",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_b:
    st.subheader("Sales & profit by region")
    by_region = f.groupby("Region", as_index=False)[["Sales", "Profit"]].sum()
    fig_region = go.Figure()
    fig_region.add_bar(name="Sales", x=by_region["Region"], y=by_region["Sales"], marker_color=COLOR_SALES)
    fig_region.add_bar(name="Profit", x=by_region["Region"], y=by_region["Profit"], marker_color=COLOR_PROFIT)
    fig_region.update_layout(
        barmode="group", height=340, margin=dict(l=0, r=10, t=10, b=10),
        yaxis_title=None, xaxis_title=None, template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickprefix="$",
    )
    st.plotly_chart(fig_region, use_container_width=True)

# profit by subcategory
st.subheader("Profit by sub-category")
st.caption(
    "The headline insight in this dataset: high sales volume does not guarantee profit. "
    "Sub-categories in red are losing money."
)
subcat = f.groupby("Sub-Category", as_index=False)[["Sales", "Profit"]].sum().sort_values("Profit")
fig_subcat = px.bar(
    subcat, x="Profit", y="Sub-Category", orientation="h",
    color=subcat["Profit"] >= 0,
    color_discrete_map={True: COLOR_POS, False: COLOR_NEG},
    hover_data={"Sales": ":$,.0f", "Profit": ":$,.0f"},
)
fig_subcat.update_layout(
    showlegend=False, height=460, margin=dict(l=0, r=10, t=10, b=10),
    xaxis_title=None, yaxis_title=None, template="plotly_white",
    xaxis_tickprefix="$",
)
st.plotly_chart(fig_subcat, use_container_width=True)

# top products 
st.subheader("Top 10 products by sales")
top = (
    f.groupby(["Product Name", "Category"], as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)
st.dataframe(
    top.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}", "Quantity": "{:,}"}),
    use_container_width=True,
    hide_index=True,
)
