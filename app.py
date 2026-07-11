import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_css, get_plotly_template, kpi_ticket

st.set_page_config(page_title="Superstore Intelligence", page_icon="📈", layout="wide")
inject_css()
TEMPLATE = get_plotly_template()

@st.cache_data
def load_raw_sales():
    df = pd.read_csv('dashboard_data/raw_sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

raw_sales = load_raw_sales()

st.markdown('<div class="eyebrow">Sales Overview</div>', unsafe_allow_html=True)
st.title("📈 Superstore Intelligence")
st.caption("4 years of transaction data · Jan 2015 – Dec 2018 · Use the sidebar to explore Forecasts, Anomalies, and Product Segments")

total_sales = raw_sales['Sales'].sum()
total_orders = raw_sales.shape[0]
avg_order = total_sales / total_orders
top_year = raw_sales.groupby('Year')['Sales'].sum().idxmax()

k1, k2, k3, k4 = st.columns(4)
kpi_ticket(k1, "Total Sales", f"${total_sales:,.0f}", "4-year total")
kpi_ticket(k2, "Transactions", f"{total_orders:,}", "line items")
kpi_ticket(k3, "Avg. Line Value", f"${avg_order:,.0f}", "per transaction")
kpi_ticket(k4, "Strongest Year", f"{top_year}", "by total sales")

st.markdown('<div class="section-label">Total Sales by Year</div>', unsafe_allow_html=True)
yearly_sales = raw_sales.groupby('Year')['Sales'].sum().reset_index()
fig_year = px.bar(yearly_sales, x='Year', y='Sales', text_auto='.2s', template=TEMPLATE)
fig_year.update_traces(marker_color='#E8A33D', marker_line_width=0)
fig_year.update_layout(height=320, showlegend=False)
st.plotly_chart(fig_year, use_container_width=True)

st.markdown('<div class="section-label">Monthly Sales Trend</div>', unsafe_allow_html=True)
monthly_sales = raw_sales.groupby(raw_sales['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order Date'] = monthly_sales['Order Date'].dt.to_timestamp()
fig_trend = px.area(monthly_sales, x='Order Date', y='Sales', template=TEMPLATE)
fig_trend.update_traces(line_color='#3DDBC4', fillcolor='rgba(61,219,196,0.12)')
fig_trend.update_layout(height=340)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown('<div class="section-label">Sales by Region & Category</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    selected_region = st.multiselect("Filter by Region", options=raw_sales['Region'].unique(), default=raw_sales['Region'].unique())
with col2:
    selected_category = st.multiselect("Filter by Category", options=raw_sales['Category'].unique(), default=raw_sales['Category'].unique())

filtered = raw_sales[(raw_sales['Region'].isin(selected_region)) & (raw_sales['Category'].isin(selected_category))]
region_cat_sales = filtered.groupby(['Region', 'Category'])['Sales'].sum().reset_index()
fig_region_cat = px.bar(region_cat_sales, x='Region', y='Sales', color='Category', barmode='group', template=TEMPLATE)
fig_region_cat.update_layout(height=380)
st.plotly_chart(fig_region_cat, use_container_width=True)