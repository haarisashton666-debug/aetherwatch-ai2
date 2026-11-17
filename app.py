
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime, timezone
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="AETHERWATCH AI",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#080b1c,#10102c,#171039);
    color: white;
}
[data-testid="stSidebar"] {
    background: #0b1025;
}
h1,h2,h3,p,label {
    color: #f2f3ff !important;
}
.metric-card {
    background: linear-gradient(135deg,#191d42,#28205a);
    border: 1px solid #6255bb;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}
.hero {
    background: linear-gradient(110deg,#171b46,#3d2472);
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #7664e8;
}
.small {
    color: #aaa9d7;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌍 AETHERWATCH")
st.sidebar.caption("EARTH INTELLIGENCE SYSTEM")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Earth Monitor",
        "Satellite Intelligence",
        "AI Detection",
        "Analytics",
        "System Status"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("AETHERWATCH AI | v1.0")

st.markdown("""
<div class="hero">
<h1>🌌 AETHERWATCH AI</h1>
<h3>The Invisible Earth Intelligence System</h3>
<p class="small">
Satellite-powered environmental intelligence
and anomaly monitoring platform.
</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=900)
def get_air_quality():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 11.0168,
        "longitude": 76.9558,
        "hourly": "pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide",
        "past_days": 2,
        "forecast_days": 1
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json()

def get_data():
    try:
        result = get_air_quality()
        hourly = result["hourly"]
        df = pd.DataFrame(hourly)
        df["time"] = pd.to_datetime(df["time"])
        return df, None
    except Exception as e:
        return None, str(e)

df, error = get_data()

if page == "Overview":
    st.subheader("Global Intelligence Overview")
    st.caption("Environmental data centre | Coimbatore observation point")

    if df is not None:
        latest = df.dropna(subset=["pm2_5"])
        latest = latest.iloc[-1] if not latest.empty else None

        if latest is not None:
            a, b, c = st.columns(3)
            a.metric("PM2.5", f"{latest['pm2_5']:.1f} µg/m³")
            b.metric("PM10", f"{latest['pm10']:.1f} µg/m³")
            c.metric("NO₂", f"{latest['nitrogen_dioxide']:.1f} µg/m³")

            st.success("Environmental data retrieved successfully")
            st.caption("Latest available observation: " +
                       str(latest["time"]))
        else:
            st.warning("No valid observations available.")
    else:
        st.warning("Environmental data unavailable: " + str(error))

    st.markdown("### Intelligence Modules")
    x, y, z = st.columns(3)
    x.info("🌍 Earth Monitoring")
    y.info("🛰️ Satellite Intelligence")
    z.info("🧠 AI Anomaly Detection")

elif page == "Earth Monitor":
    st.subheader("Earth Observation Centre")
    st.markdown("**Monitoring location: Coimbatore, India**")

    st.map(pd.DataFrame({
        "lat": [11.0168],
        "lon": [76.9558]
    }))

    st.write("Observation coordinates: 11.0168° N, 76.9558° E")

elif page == "Satellite Intelligence":
    st.subheader("Satellite Intelligence Centre")
    st.info(
        "Satellite data integration is the next development module. "
        "The current dashboard uses public atmospheric data, "
        "not direct satellite observations."
    )

    st.write("Planned datasets: Sentinel-5P and NASA Earthdata.")

elif page == "AI Detection":
    st.subheader("AI Environmental Anomaly Detection")

    if df is not None:
        features = [
            "pm2_5",
            "pm10",
            "nitrogen_dioxide",
            "sulphur_dioxide"
        ]

        clean = df[features].dropna()

        if len(clean) >= 10:
            model = IsolationForest(
                contamination=0.05,
                random_state=42
            )
            predictions = model.fit_predict(clean)
            clean = clean.copy()
            clean["status"] = np.where(
                predictions == -1,
                "Unusual pattern",
                "Normal pattern"
            )

            st.write("AI analysis of available environmental readings")
            st.dataframe(clean.tail(20), use_container_width=True)

            unusual = int((predictions == -1).sum())
            st.metric("Unusual observations detected", unusual)
            st.caption(
                "Exploratory anomaly detection, not a verified "
                "pollution event or safety warning."
            )
        else:
            st.warning("Not enough valid data for AI analysis.")
    else:
        st.warning("Cannot run analysis without source data.")

elif page == "Analytics":
    st.subheader("Environmental Analytics")

    if df is not None:
        metric = st.selectbox(
            "Choose environmental parameter",
            [
                "pm2_5",
                "pm10",
                "nitrogen_dioxide",
                "sulphur_dioxide"
            ]
        )

        chart = px.line(
            df,
            x="time",
            y=metric,
            title=metric.upper() + " Observation History",
            template="plotly_dark"
        )
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.warning("No source data available.")

elif page == "System Status":
    st.subheader("Platform System Status")

    st.write("Application: AETHERWATCH AI")
    st.write("Version: 1.0")
    st.write("Runtime: Streamlit")
    st.write("Data source: Open-Meteo Air Quality API")
    st.write("Current UTC time:", datetime.now(timezone.utc).isoformat())

    if df is not None:
        st.success("Data service: Connected")
    else:
        st.error("Data service: Unavailable")

    st.info("Refresh the application to request fresh observations.")

st.markdown("---")
st.caption("AETHERWATCH AI | Environmental Intelligence Platform")
st.caption("Public data may be delayed, revised or unavailable.")
                   
