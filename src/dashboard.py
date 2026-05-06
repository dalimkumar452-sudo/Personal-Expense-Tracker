import streamlit as st
import plotly.express as px
import pandas as pd
import os
from datetime import datetime
from database import initialize_database, save_to_db, load_all_data

# Page Configuration for Wide Layout
st.set_page_config(
    page_title="Personal Finance Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
initialize_database()

# --- PROFESSIONAL CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1c2128 !important;
        border: 1px solid #30363d !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }
    /* Metric Text Colors */
    div[data-testid="stMetricValue"] > div {
        color: #58a6ff !important;
        font-weight: 700 !important;
    }
    /* Custom Sidebar Header */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #c9d1d9;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UTILITY FUNCTIONS ---
def get_conversions(amount):
    return {
        'BDT': amount * 1.35,
        'USD': amount * 0.012,
        'EUR': amount_inr * 0.011 if 'amount_inr' in locals() else amount * 0.011
    }

# --- SIDEBAR: SMART FILTERS ---
with st.sidebar:
    st.markdown('<p class="sidebar-header">📊 Smart Filters</p>', unsafe_allow_html=True)
    
    # User Input Section
    with st.expander("➕ Add New Transaction", expanded=False):
        d = st.date_input("Date", datetime.now())
        cat = st.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Education"])
        amt = st.number_input("Amount", min_value=0.0)
        meth = st.selectbox("Method", ["bKash", "Paytm", "Cash", "Card"])
        if st.button("Sync to Intelligence"):
            save_to_db(d.strftime("%Y-%m-%d"), cat, amt, "INR", meth, "Manual Entry")
            st.rerun()

    st.markdown("---")
    # Multi-select filters (like in your reference image)
    df = load_all_data()
    if not df.empty:
        selected_cat = st.multiselect("Filter Category", df['category'].unique(), default=df['category'].unique())
        selected_meth = st.multiselect("Filter Method", df['method'].unique(), default=df['method'].unique())
        filtered_df = df[(df['category'].isin(selected_cat)) & (df['method'].isin(selected_meth))]
    else:
        filtered_df = df

# --- MAIN DASHBOARD AREA ---
st.title("📈 Personal Finance Intelligence Dashboard")
st.caption("Advanced Real-time Analytics & Multi-Currency Tracking")

if not filtered_df.empty:
    # 1. KPI Metrics Row
    total = filtered_df['amount'].sum()
    conv = get_conversions(total)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Liquidity (INR)", f"₹{total:,.2f}")
    m2.metric("Intelligence (BDT)", f"৳{conv['BDT']:,.2f}")
    m3.metric("Global (USD)", f"${conv['USD']:,.2f}")
    m4.metric("Market (EUR)", f"€{conv['EUR']:,.2f}")

    st.markdown("---")

    # 2. Analytics Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧬 Spending Segmentation")
        # Multi-color donut chart
        fig_pie = px.pie(
            filtered_df, values='amount', names='category',
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📊 Method Distribution")
        # Bar chart with gradient-like colors
        fig_bar = px.bar(
            filtered_df.groupby('method')['amount'].sum().reset_index(),
            x='method', y='amount',
            color='amount',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. Intelligence Audit Trail (Data Table)
    st.subheader("📑 Intelligence Audit Trail")
    st.dataframe(filtered_df.sort_values('date', ascending=False), use_container_width=True)

else:
    st.info("System waiting for data. Please add a transaction in the sidebar.")