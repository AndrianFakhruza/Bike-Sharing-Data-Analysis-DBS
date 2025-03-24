import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm

# Konfigurasi Tampilan Streamlit
st.set_page_config(page_title="🚲 Dashboard Penyewaan Sepeda", layout="wide")

# Menentukan path file
base_path = os.path.dirname(os.path.abspath(__file__))
day_file = os.path.join(base_path, "day.csv")
hour_file = os.path.join(base_path, "hour.csv")

# Memeriksa apakah file tersedia
if not os.path.exists(day_file) or not os.path.exists(hour_file):
    st.error("❌ File dataset tidak ditemukan! Pastikan file 'day.csv' dan 'hour.csv' tersedia.")
    st.stop()

# Pilihan dataset
data_option = st.sidebar.radio("📂 Pilih Dataset", ["Per Hari", "Per Jam"])
df = pd.read_csv(day_file if data_option == "Per Hari" else hour_file)

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
season_map = {1: "🌱 Musim Semi", 2: "☀️ Musim Panas", 3: "🍂 Musim Gugur", 4: "❄️ Musim Dingin"}
weather_map = {1: "☀️ Cerah", 2: "⛅ Berawan", 3: "🌧️ Hujan", 4: "❄️ Salju"}

df['season'] = df['season'].map(season_map)
df['weathersit'] = df['weathersit'].map(weather_map)

season = st.sidebar.selectbox("🌎 Pilih Musim", ["Semua"] + df['season'].dropna().unique().tolist())
weather = st.sidebar.selectbox("🌦️ Pilih Cuaca", ["Semua"] + df['weathersit'].dropna().unique().tolist())

# Filter data
filtered_df = df.copy()
if season != "Semua":
    filtered_df = filtered_df[filtered_df['season'] == season]
if weather != "Semua":
    filtered_df = filtered_df[filtered_df['weathersit'] == weather]

# Layout dashboard
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("**Analisis penyewaan sepeda berdasarkan musim, cuaca, dan kecepatan angin.**")

# Metrik utama
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("📉 Rata-rata Penyewaan", f"{filtered_df['cnt'].mean():,.2f}")
with col3:
    st.metric("🚀 Penyewaan Tertinggi", f"{filtered_df['cnt'].max():,}")
with col4:
    st.metric("🐢 Penyewaan Terendah", f"{filtered_df['cnt'].min():,}")

# Grafik Penyewaan Berdasarkan Musim
st.subheader("📅 Penyewaan Sepeda Berdasarkan Musim")
seasonal_rentals = filtered_df.groupby('season')['cnt'].sum().reset_index()
fig_season = px.bar(seasonal_rentals, x='season', y='cnt', color='season', title="Penyewaan Berdasarkan Musim", color_discrete_sequence=["blue"])
st.plotly_chart(fig_season, use_container_width=True)

# Grafik Pengaruh Cuaca
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")
weather_rentals = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
fig_weather = px.bar(weather_rentals, x='weathersit', y='cnt', color='weathersit', title="Rata-rata Penyewaan Berdasarkan Cuaca", color_discrete_sequence=["blue"])
st.plotly_chart(fig_weather, use_container_width=True)

# Grafik Hubungan Kecepatan Angin dan Penyewaan
st.subheader("💨 Pengaruh Kecepatan Angin terhadap Penyewaan")
if 'windspeed' in filtered_df.columns:
    fig_wind = px.scatter(filtered_df, x='windspeed', y='cnt', color='cnt',
                          title="Hubungan Kecepatan Angin dengan Penyewaan",
                          labels={'windspeed': "Kecepatan Angin", 'cnt': "Jumlah Penyewaan"},
                          trendline="ols")
    st.plotly_chart(fig_wind, use_container_width=True)
else:
    st.warning("⚠️ Data tidak memiliki kolom 'windspeed'.")

# Grafik Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda")
if data_option == "Per Hari":
    fig_trend = px.line(filtered_df, x='dteday', y='cnt', title="Tren Penyewaan Sepeda per Hari")
else:
    fig_trend = px.line(filtered_df, x='hr', y='cnt', title="Tren Penyewaan Sepeda per Jam", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# Kesimpulan
st.subheader("🎯 Kesimpulan dan Rekomendasi")
st.markdown("""
- 🚴 Penyewaan sepeda lebih tinggi pada musim panas dibandingkan musim lainnya.
- 🌦️ Cuaca buruk seperti hujan dan salju mengurangi jumlah penyewaan.
- 💨 Kecepatan angin berpengaruh terhadap pola penyewaan.
- 📌 Manajemen armada bisa disesuaikan berdasarkan tren musiman dan cuaca.
""")