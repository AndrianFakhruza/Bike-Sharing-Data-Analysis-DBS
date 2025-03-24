import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Load dataset
base_path = os.path.dirname(os.path.abspath(__file__))  # Path dari file dashboard.py
file_path = os.path.join(base_path, "all_data.csv")  # Gabungkan path
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
st.markdown("Analisis data penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, dan waktu.")

# Key Metrics
total_rentals = filtered_df['cnt_hour'].sum()
daily_avg = round(filtered_df['cnt_hour'].mean(), 2)
max_rental = filtered_df['cnt_hour'].max()
min_rental = filtered_df['cnt_hour'].min()
max_date = filtered_df.loc[filtered_df['cnt_hour'].idxmax(), 'dteday']
min_date = filtered_df.loc[filtered_df['cnt_hour'].idxmin(), 'dteday']

st.subheader("📊 Metrik Utama")
st.metric("Total Penyewaan", f"{total_rentals:,}")
st.metric("Rata-rata per Hari", f"{daily_avg:,}")
st.metric("Penyewaan Tertinggi", f"{max_rental:,}", help=f"Pada {max_date}")
st.metric("Penyewaan Terendah", f"{min_rental:,}", help=f"Pada {min_date}")

# Rentals per hour
time_series = filtered_df.groupby('hr')['cnt_hour'].sum().reset_index()
st.subheader("⏰ Jumlah Penyewaan Berdasarkan Jam")
fig_hourly = px.bar(time_series, x='hr', y='cnt_hour', title="Jumlah Penyewaan Berdasarkan Jam")
st.plotly_chart(fig_hourly)

# Seasonal Rentals
seasonal_rentals = filtered_df.groupby('season_hour')['cnt_hour'].sum().reset_index()
st.subheader("🍂 Penyewaan Berdasarkan Musim")
fig_season = px.bar(seasonal_rentals, x='season_hour', y='cnt_hour', title="Penyewaan Berdasarkan Musim")
st.plotly_chart(fig_season)

# Weather impact
weather_rentals = filtered_df.groupby('weathersit_hour')['cnt_hour'].mean().reset_index()
st.subheader("🌤️ Pengaruh Cuaca Terhadap Penyewaan")
fig_weather = px.bar(weather_rentals, x='weathersit_hour', y='cnt_hour', title="Rata-rata Penyewaan Berdasarkan Cuaca")
st.plotly_chart(fig_weather)

st.subheader("🎯 Kesimpulan dan Rekomendasi")
st.markdown("""
- Cuaca sangat memengaruhi penyewaan sepeda. Saat cerah, penyewaan tinggi, menurun saat mendung, dan drastis berkurang saat hujan.
- Dalam sehari, penyewaan memuncak pukul 17:00, kemungkinan karena jam pulang kerja. Lonjakan juga terjadi pukul 08:00-09:00 saat orang berangkat kerja atau sekolah.
""")