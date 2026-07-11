import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_css, get_plotly_template, kpi_ticket

st.set_page_config(page_title="Product Demand Segments", page_icon="🧩", layout="wide")
inject_css()
TEMPLATE = get_plotly_template()

@st.cache_data
def load_clusters():
    return pd.read_csv('dashboard_data/clusters.csv')

features = load_clusters()

st.markdown('<div class="eyebrow">Method: K-Means (K=4) + PCA</div>', unsafe_allow_html=True)
st.title("🧩 Product Demand Segments")
st.caption("17 sub-categories grouped by total sales, growth rate, volatility, and average order value")

k1, k2, k3, k4 = st.columns(4)
cluster_counts = features['Cluster_Label'].value_counts()
for col, label in zip([k1, k2, k3, k4], cluster_counts.index):
    kpi_ticket(col, label, f"{cluster_counts[label]}", "sub-categories")

st.markdown('<div class="section-label">Cluster Map (PCA-reduced)</div>', unsafe_allow_html=True)

fig = px.scatter(features, x='PCA1', y='PCA2', color='Cluster_Label', text='Sub-Category', template=TEMPLATE, size='Total_Sales', size_max=40)
fig.update_traces(textposition='top center', textfont=dict(size=10, color='#F2F1ED'))
fig.update_layout(height=520, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-label">Sub-Categories by Cluster</div>', unsafe_allow_html=True)

selected_cluster = st.selectbox("Filter by cluster", options=['All'] + sorted(features['Cluster_Label'].unique().tolist()))
table_data = features if selected_cluster == 'All' else features[features['Cluster_Label'] == selected_cluster]

display_cols = ['Sub-Category', 'Cluster_Label', 'Total_Sales', 'Growth_Rate_%', 'Volatility', 'Avg_Order_Value']
st.dataframe(table_data[display_cols].sort_values('Total_Sales', ascending=False).round(1), use_container_width=True, hide_index=True)