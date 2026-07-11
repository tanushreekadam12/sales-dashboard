import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from style import inject_css, get_plotly_template, kpi_ticket

st.set_page_config(page_title="Anomaly Report", page_icon="🚨", layout="wide")
inject_css()
TEMPLATE = get_plotly_template()

@st.cache_data
def load_anomalies():
    df = pd.read_csv('dashboard_data/weekly_anomalies.csv')
    df['Week'] = pd.to_datetime(df['Week'])
    return df

weekly_df = load_anomalies()
anomalies = weekly_df[weekly_df['iso_anomaly'] == -1].sort_values('Week')

st.markdown('<div class="eyebrow">Method: Isolation Forest</div>', unsafe_allow_html=True)
st.title("🚨 Anomaly Report")
st.caption("Unusually high or low sales weeks, flagged using Isolation Forest on 4 years of weekly totals")

k1, k2, k3 = st.columns(3)
kpi_ticket(k1, "Weeks Flagged", f"{len(anomalies)}", "out of 209 weeks")
kpi_ticket(k2, "Highest Anomaly", f"${anomalies['Sales'].max():,.0f}", anomalies.loc[anomalies['Sales'].idxmax(), 'Week'].strftime('%b %d, %Y'))
kpi_ticket(k3, "Lowest Anomaly", f"${anomalies['Sales'].min():,.0f}", anomalies.loc[anomalies['Sales'].idxmin(), 'Week'].strftime('%b %d, %Y'))

st.markdown('<div class="section-label">Weekly Sales with Flagged Anomalies</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=weekly_df['Week'], y=weekly_df['Sales'], mode='lines', name='Weekly Sales', line=dict(color='#5DA9E8', width=1.5)))
fig.add_trace(go.Scatter(x=anomalies['Week'], y=anomalies['Sales'], mode='markers', name='Anomaly', marker=dict(color='#E85D75', size=12, symbol='circle', line=dict(color='#12141C', width=1))))
fig.update_layout(template=TEMPLATE, height=440, hovermode='closest', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-label">Detected Anomaly Dates</div>', unsafe_allow_html=True)
anomaly_table = anomalies[['Week', 'Sales']].copy()
anomaly_table['Week'] = anomaly_table['Week'].dt.strftime('%b %d, %Y')
anomaly_table['Sales'] = anomaly_table['Sales'].round(0)
anomaly_table['Type'] = anomaly_table['Sales'].apply(lambda x: 'High Spike' if x > weekly_df['Sales'].median() else 'Low Dip')
st.dataframe(anomaly_table.reset_index(drop=True), use_container_width=True, hide_index=True)