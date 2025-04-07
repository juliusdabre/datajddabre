
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Load CSV instead of Excel
df = pd.read_csv("propwealthnext_investor_cleaned_display.csv")

# Sidebar filters
st.sidebar.header("🎯 Filter for Investor Research")
score_range = st.sidebar.slider("Investor Score Range", 0, 100, (60, 100))
selected_state = st.sidebar.multiselect("Filter by State", df["State"].dropna().unique(), default=df["State"].dropna().unique())
selected_type = st.sidebar.multiselect("Property Type", df["Property\nType"].dropna().unique(), default=df["Property\nType"].dropna().unique())

# Apply filters
filtered_df = df[
    (df["Investor Score (Out Of 100)"].between(score_range[0], score_range[1])) &
    (df["State"].isin(selected_state)) &
    (df["Property\nType"].isin(selected_type))
]

st.title("🏡 Smart Investor Dashboard (CSV-Based)")

# Suburb selector
selected_suburb = st.selectbox("📍 Choose a Suburb", filtered_df["Suburb"].unique())

# Display metrics
if selected_suburb:
    row = filtered_df[filtered_df["Suburb"] == selected_suburb].iloc[0]
    st.markdown(f"""
    ### 📌 Investor Metrics: {selected_suburb}
    <div style='line-height: 2.2; font-size: 18px;'>
    💰 <b>Investor Score</b>: {row['Investor Score (Out Of 100)']}<br>
    📈 <b>10 Year Growth</b>: {row['10 Year Growth']}%<br>
    🔥 <b>Growth Gap Index</b>: {row['Growth Gap Index']}<br>
    💸 <b>Yield</b>: {row['Yield']}%<br>
    🧮 <b>Buy Affordability</b>: {row['Buy Affordability (Years)']} yrs<br>
    📉 <b>Rent Affordability</b>: {row['Rent Affordability (% Of Income)']}%
    </div>
    """, unsafe_allow_html=True)

# Geo Map
st.subheader("🗺️ Suburb Map Based on Investor Score")
fig = px.scatter_map(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Investor Score (Out Of 100)",
    size="Growth Gap Index",
    hover_name="Suburb",
    zoom=4,
    height=500,
    title="Investor Score by Location",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig)

# Heatmap
st.subheader("🔥 Correlation Heatmap")
heat_cols = [
    "Investor Score (Out Of 100)", "Growth Gap Index", "10 Year Growth",
    "Yield", "Buy Affordability (Years)", "Rent Affordability (% Of Income)"
]
corr = filtered_df[heat_cols].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    label="📥 Download Heatmap as PNG",
    data=buf.getvalue(),
    file_name="heatmap_raw_investor_metrics.png",
    mime="image/png"
)
