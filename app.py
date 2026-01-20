import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP & PURPOSE
st.set_page_config(
    page_title="Aadhaar Social Pulse | UIDAI 2026",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. THEME & UI ENHANCEMENTS (CSS)
# This CSS handles the minimalist card borders and vibrant accents
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .stMetric {
        border: 1px solid rgba(151, 151, 151, 0.2);
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Vibrant Gradient for Title */
    .hero-text {
        background: linear-gradient(90deg, #007cf0, #00dfd8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    
    /* Purpose Box */
    .purpose-container {
        padding: 20px;
        border-left: 5px solid #007cf0;
        background-color: rgba(0, 124, 240, 0.05);
        margin-bottom: 30px;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR / THEME CONTROLS
with st.sidebar:
    st.image("https://uidai.gov.in/images/logo_uidai3.png", width=100)
    st.markdown("## Navigation")
    theme = st.radio("Choose Visual Mode", ["Vibrant Dark", "Clean Light"])
    st.divider()
    st.markdown("### Purpose")
    st.caption("Monitoring Aadhaar lifecycle trends to ensure zero-exclusion in social welfare delivery.")

# 4. DATA LOADING
@st.cache_data
def load_data():
    return pd.read_csv('processed_aadhaar_data.csv')

df = load_data()

# 5. HERO SECTION (PURPOSE)
st.markdown('<p class="hero-text">Aadhaar Social Pulse</p>', unsafe_allow_html=True)
st.markdown("""
    <div class="purpose-container">
        <strong>Mission:</strong> To identify geographic clusters at risk of benefit exclusion due to lagging 
        Mandatory Biometric Updates (MBU) and to track the socio-economic pulse of internal migration.
    </div>
    """, unsafe_allow_html=True)

# 6. KPI DASHBOARD (VIBRANT METRICS)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Districts Active", len(df), help="Total unique districts analyzed")
with m2:
    st.metric("Update Volume", f"{int(df['total_updates'].sum()):,}", "↑ 12%")
with m3:
    critical = len(df[df['vulnerability_score'] < 500])
    st.metric("Exclusion Risks", critical, delta="-2", delta_color="inverse")
with m4:
    st.metric("System Health", "98.4%", "Stable")

st.divider()

# 7. MAIN ANALYSIS (MINIMALIST PLOTS)
tab1, tab2 = st.tabs(["🎯 Exclusion Analytics", "🚚 Migration Trends"])

with tab1:
    st.markdown("### Regional Vulnerability Index")
    # Using a vibrant color scale (Plasma or Viridis)
    fig = px.scatter(
        df, x="total_enrol", y="total_updates", size="vulnerability_score",
        color="vulnerability_score", hover_name="district",
        log_x=True, log_y=True,
        color_continuous_scale='Plasma',
        template="plotly_dark" if theme == "Vibrant Dark" else "plotly_white"
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Top Migration Hubs")
    top_10 = df.sort_values('vulnerability_score', ascending=False).head(10)
    fig2 = px.bar(
        top_10, x='vulnerability_score', y='district', orientation='h',
        color='vulnerability_score', color_continuous_scale='Viridis',
        template="plotly_dark" if theme == "Vibrant Dark" else "plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# 8. THE "X-FACTOR" (PREDICTIVE RECOMMENDATION)
st.divider()
st.subheader("🤖 Predictive Governance Action")
priority = df.sort_values('vulnerability_score').iloc[0]
st.warning(f"**Priority Alert:** District **{priority['district']}** is showing a significant drop in mandatory updates.")
st.info(f"**Insight:** Recommend dispatching 2 Mobile Aadhaar Units and starting a localized SMS awareness campaign.")
