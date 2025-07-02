
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("dynamic_pricing_uber_style.csv")

st.title("Dynamic Pricing Strategy Dashboard – Uber/Ola Style")
st.markdown("Compare standard dynamic pricing with Uber-style peak-hour surge pricing.")

# Filters
season = st.selectbox("Select Season", ["All"] + df["season"].unique().tolist())
time = st.selectbox("Select Time of Day", ["All"] + df["time_of_day"].unique().tolist())
segment = st.selectbox("Select User Segment", ["All"] + df["user_segment"].unique().tolist())

# Apply filters
filtered_df = df.copy()
if season != "All":
    filtered_df = filtered_df[filtered_df["season"] == season]
if time != "All":
    filtered_df = filtered_df[filtered_df["time_of_day"] == time]
if segment != "All":
    filtered_df = filtered_df[filtered_df["user_segment"] == segment]

# Pricing model selection
pricing_option = st.radio("Select Pricing Model", ["Standard", "Uber/Ola Peak Hour Pricing"])

price_column = "dynamic_price" if pricing_option == "Standard" else "dynamic_price_uber"

# Metrics
st.metric("Average Base Price", f"₹{filtered_df['base_price'].mean():.2f}")
st.metric(f"Average {pricing_option} Price", f"₹{filtered_df[price_column].mean():.2f}")

# Line Chart
st.subheader("Price Trend Over Time")
st.line_chart(filtered_df.set_index("timestamp")[["base_price", price_column]])

# Price Distribution
st.subheader("Price Distribution")
sample_size = min(20, len(filtered_df))
st.bar_chart(filtered_df[["base_price", price_column]].sample(sample_size).reset_index(drop=True))

# Show peak info if Uber-style selected
if pricing_option == "Uber/Ola Peak Hour Pricing":
    st.markdown("Note: A 1.4x multiplier is applied during peak hours (7–10 AM, 5–8 PM).")

# Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
