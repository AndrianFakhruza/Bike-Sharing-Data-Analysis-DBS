import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "all_data.csv")
df = pd.read_csv(file_path)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + sorted(df['yr_hour'].unique().tolist()))
season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + sorted(df['season_hour'].unique().tolist()))
day_type = st.sidebar.selectbox("Pilih Tipe Hari", ["Semua", "Weekday", "Weekend"])
weather = st.sidebar.selectbox("Pilih Cuaca", ["Semua"] + sorted(df['weathersit_hour'].unique().tolist()))
month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + sorted(df['mnth_hour'].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if year != "Semua":
    filtered_df = filtered_df[filtered_df['yr_hour'] == year]
if season != "Semua":
    filtered_df = filtered_df[filtered_df['season_hour'] == season]
if day_type != "Semua":
    if day_type == "Weekday":
        filtered_df = filtered_df[filtered_df['weekday_hour'] < 6]
    else:
        filtered_df = filtered_df[filtered_df['weekday_hour'] >= 6]
if weather != "Semua":
    filtered_df = filtered_df[filtered_df['weathersit_hour'] == weather]
if month != "Semua":
    filtered_df = filtered_df[filtered_df['mnth_hour'] == month]

# Main Dashboard Title
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("Analisis penyewaan sepeda berdasarkan berbagai faktor.")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{filtered_df['cnt_hour'].sum():,}")
col2.metric("Rata-rata per Hari", f"{filtered_df['cnt_hour'].mean():,.2f}")
col3.metric("Tertinggi", f"{filtered_df['cnt_hour'].max():,}")
col4.metric("Terendah", f"{filtered_df['cnt_hour'].min():,}")

# User proportion
st.subheader("👥 Proporsi Pengguna")
fig, ax = plt.subplots()
labels = ["Terdaftar", "Casual"]
sizes = [filtered_df['registered_hour'].sum(), filtered_df['casual_hour'].sum()]
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
st.pyplot(fig)

# Rentals per hour
st.subheader("⏰ Penyewaan Berdasarkan Jam")
time_series = filtered_df.groupby('hr')['cnt_hour'].sum().reset_index()
st.plotly_chart(px.bar(time_series, x='hr', y='cnt_hour', title="Jumlah Penyewaan Berdasarkan Jam", color_discrete_sequence=['#636EFA']))

# Seasonal Rentals
st.subheader("🍂 Penyewaan Berdasarkan Musim")
seasonal_rentals = filtered_df.groupby('season_hour')['cnt_hour'].sum().reset_index()
st.plotly_chart(px.bar(seasonal_rentals, x='season_hour', y='cnt_hour', title="Penyewaan Berdasarkan Musim", color_discrete_sequence=['#EF553B']))

# Weather impact
st.subheader("🌤️ Pengaruh Cuaca")
weather_rentals = filtered_df.groupby('weathersit_hour')['cnt_hour'].mean().reset_index()
st.plotly_chart(px.bar(weather_rentals, x='weathersit_hour', y='cnt_hour', title="Penyewaan Berdasarkan Cuaca", color_discrete_sequence=['#00CC96']))

# Conclusion
st.subheader("🎯 Kesimpulan & Rekomendasi")
st.markdown("""
- **Pola penyewaan** terlihat meningkat pada jam tertentu.
- **Cuaca & Musim** sangat berpengaruh terhadap jumlah penyewaan.
- **Strategi promosi** dapat diarahkan pada musim dengan penyewaan rendah.
""")
