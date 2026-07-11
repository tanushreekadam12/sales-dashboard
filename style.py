import streamlit as st
import plotly.graph_objects as go

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #12141C;
        color: #F2F1ED;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #F2F1ED !important;
    }

    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    .eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #E8A33D;
        margin-bottom: -0.6rem;
    }

    .section-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #F2F1ED;
        border-left: 3px solid #E8A33D;
        padding-left: 0.6rem;
        margin: 1.8rem 0 0.8rem 0;
    }

    .ticket {
        background: #1A1D2B;
        border: 1px dashed #3A3E52;
        border-radius: 6px;
        padding: 1rem 1.2rem;
    }
    .ticket-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8A8D9E;
        margin-bottom: 0.3rem;
    }
    .ticket-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #E8A33D;
    }
    .ticket-sub {
        font-size: 0.78rem;
        color: #3DDBC4;
        margin-top: 0.2rem;
    }

    .pill {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .pill-amber { background: rgba(232,163,61,0.15); color: #E8A33D; }
    .pill-teal  { background: rgba(61,219,196,0.15); color: #3DDBC4; }
    .pill-red   { background: rgba(232,93,117,0.15); color: #E85D75; }
    .pill-purple{ background: rgba(138,111,232,0.15); color: #8A6FE8; }

    section[data-testid="stSidebar"] {
        background: #171926;
        border-right: 1px solid #262A3D;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background-color: #E8A33D !important;
        color: #12141C !important;
    }

    hr { border-color: #262A3D !important; }

    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #E8A33D;
    }
    </style>
    """, unsafe_allow_html=True)


def get_plotly_template():
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor="#12141C",
        plot_bgcolor="#12141C",
        font=dict(family="Inter, sans-serif", color="#F2F1ED", size=13),
        colorway=["#E8A33D", "#3DDBC4", "#8A6FE8", "#E85D75", "#5DA9E8"],
        xaxis=dict(gridcolor="#262A3D", zerolinecolor="#262A3D"),
        yaxis=dict(gridcolor="#262A3D", zerolinecolor="#262A3D"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=30, l=10, r=10, b=10),
    )
    return template


def kpi_ticket(col, label, value, sub):
    with col:
        st.markdown(f"""
        <div class="ticket">
            <div class="ticket-label">{label}</div>
            <div class="ticket-value">{value}</div>
            <div class="ticket-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)