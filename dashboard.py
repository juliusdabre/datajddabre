
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

st.title(" Investors score")

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
st.subheader(" Correlation Heatmap")
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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv("propwealthnext_investor_cleaned_display.csv")

# Select a few example suburbs to compare
suburbs_to_compare = df["Suburb"].dropna().unique()[:3]
metrics = [
    "Investor Score (Out Of 100)", "Growth Gap Index", "10 Year Growth",
    "Yield", "Buy Affordability (Years)", "Rent Affordability (% Of Income)"
]

# Normalize data for better radar comparison
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Setup radar chart structure
angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # loop back to start

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
colors = ['#FF5733', '#2980B9', '#27AE60']

for i, suburb in enumerate(suburbs_to_compare):
    row = df[df["Suburb"] == suburb][metrics].iloc[0]
    values = [normalize(df[m])[df["Suburb"] == suburb].values[0] for m in metrics]
    values += values[:1]  # repeat first to close loop
    ax.plot(angles, values, label=suburb, linewidth=2, color=colors[i])
    ax.fill(angles, values, alpha=0.25, color=colors[i])

# Styling
ax.set_title("🏙️ Investment Metric Radar Chart", fontsize=16, pad=20)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics, fontsize=10)
ax.set_yticklabels([])
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.savefig("radar_chart_investor_metrics.png", dpi=300)
