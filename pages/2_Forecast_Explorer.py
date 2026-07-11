import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from style import inject_css, get_plotly_template, kpi_ticket

st.set_page_config(page_title="Forecast Explorer", page_icon="🔮", layout="wide")
inject_css()
TEMPLATE = get_plotly_template()

@st.cache_data
def load_forecasts():
    df = pd.read_csv('dashboard_data/forecasts.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

forecasts = load_forecasts()

st.markdown('<div class="eyebrow">Model: SARIMA (best performer, Task 3)</div>', unsafe_allow_html=True)
st.title("🔮 Forecast Explorer")
st.caption("3-month SARIMA forecasts for each product category and region, benchmarked against actual Oct–Dec 2018 sales")

col1, col2 = st.columns([2, 3])
with col1:
    segment = st.selectbox("Select Category or Region", options=sorted(forecasts['Segment'].unique()))
with col2:
    horizon = st.select_slider("Forecast horizon (months ahead)", options=[1, 2, 3], value=3)

seg_data = forecasts[(forecasts['Segment'] == segment) & (forecasts['Month_Ahead'] <= horizon)].sort_values('Date')

mae = seg_data['MAE'].iloc[0]
rmse = seg_data['RMSE'].iloc[0]
mape = seg_data['MAPE'].iloc[0]

k1, k2, k3 = st.columns(3)
kpi_ticket(k1, "MAE", f"${mae:,.0f}", "avg. dollar error")
kpi_ticket(k2, "RMSE", f"${rmse:,.0f}", "penalizes big misses")
kpi_ticket(k3, "MAPE", f"{mape:.2f}%", "avg. % error")

st.markdown('<div class="section-label">Actual vs. Forecasted Sales</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=seg_data['Date'], y=seg_data['Actual'], mode='lines+markers', name='Actual', line=dict(color='#3DDBC4', width=3), marker=dict(size=9)))
fig.add_trace(go.Scatter(x=seg_data['Date'], y=seg_data['Forecast'], mode='lines+markers', name='Forecast', line=dict(color='#E8A33D', width=3, dash='dash'), marker=dict(size=9, symbol='x')))
fig.update_layout(template=TEMPLATE, height=420, hovermode='x unified', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-label">Forecast Detail</div>', unsafe_allow_html=True)
display_table = seg_data[['Month_Ahead', 'Date', 'Actual', 'Forecast']].copy()
display_table['Miss ($)'] = (display_table['Actual'] - display_table['Forecast']).round(0)
display_table['Miss (%)'] = ((display_table['Actual'] - display_table['Forecast']) / display_table['Actual'] * 100).round(1)
display_table['Date'] = display_table['Date'].dt.strftime('%b %Y')
st.dataframe(display_table, use_container_width=True, hide_index=True)