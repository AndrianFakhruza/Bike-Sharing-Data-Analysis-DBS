import os
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# =========================[ Load Dataset ]=========================
# Dapatkan path dari script saat ini
base_path = os.path.dirname(os.path.abspath(__file__))

# Gabungkan path dengan nama file
file_day = os.path.join(base_path, "day.csv")
file_hour = os.path.join(base_path, "hour.csv")

# Cek apakah file ada
if os.path.exists(file_day) and os.path.exists(file_hour):
    df_day = pd.read_csv(file_day)
    df_hour = pd.read_csv(file_hour)
    st.success("✅ Data berhasil dimuat!")
else:
    st.error("❌ Error: File day.csv atau hour.csv tidak ditemukan! Periksa kembali path-nya.")
    st.stop()

# =====================[ Sidebar - Filter Data ]=====================
st.sidebar.header("🔍 Filter Data")

year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + sorted(df_day['yr'].unique().tolist()))
season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + sorted(df_day['season'].unique().tolist()))
weather = st.sidebar.selectbox("Pilih Cuaca", ["Semua"] + sorted(df_hour['weathersit'].unique().tolist()))
month = st.sidebar.selectbox("Pilih Bulan", ["Semua"] + sorted(df_day['mnth'].unique().tolist()))

# Filter Data
filtered_day = df_day.copy()
filtered_hour = df_hour.copy()

if year != "Semua":
    filtered_day = filtered_day[filtered_day['yr'] == year]
    filtered_hour = filtered_hour[filtered_hour['yr'] == year]
if season != "Semua":
    filtered_day = filtered_day[filtered_day['season'] == season]
if weather != "Semua":
    filtered_hour = filtered_hour[filtered_hour['weathersit'] == weather]
if month != "Semua":
    filtered_day = filtered_day[filtered_day['mnth'] == month]

# ===================[ Main Dashboard Title ]===================
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("📊 **Analisis penyewaan sepeda berdasarkan musim, cuaca, dan faktor lingkungan.**")

# =====================[ Key Metrics ]======================
total_rentals = filtered_day['cnt'].sum()
daily_avg = round(filtered_day['cnt'].mean(), 2)
max_rental = filtered_day['cnt'].max()
min_rental = filtered_day['cnt'].min()
max_date = filtered_day.loc[filtered_day['cnt'].idxmax(), 'dteday']
min_date = filtered_day.loc[filtered_day['cnt'].idxmin(), 'dteday']

st.subheader("📊 Metrik Utama")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Rata-rata per Hari", f"{daily_avg:,}")
col3.metric("Penyewaan Tertinggi", f"{max_rental:,}", help=f"Pada {max_date}")
col4.metric("Penyewaan Terendah", f"{min_rental:,}", help=f"Pada {min_date}")

# =====================[ Proporsi Pengguna ]=======================
total_registered = filtered_day['registered'].sum()
total_casual = filtered_day['casual'].sum()
total_users = total_registered + total_casual

st.subheader("👥 Proporsi Pengguna")
fig_pie = px.pie(
    names=["Terdaftar", "Casual"], 
    values=[total_registered, total_casual], 
    title="Proporsi Pengguna Terdaftar vs Casual",
    color_discrete_sequence=["#636EFA", "#EF553B"]
)
st.plotly_chart(fig_pie)

# =====================[ Rentals per Hour ]=======================
time_series = filtered_hour.groupby('hr')['cnt'].sum().reset_index()
st.subheader("⏰ Jumlah Penyewaan Berdasarkan Jam")
fig_hourly = px.line(
    time_series, x='hr', y='cnt', 
    title="Tren Penyewaan Sepeda Berdasarkan Jam", 
    markers=True,
    color_discrete_sequence=["#00CC96"]
)
st.plotly_chart(fig_hourly)

# ===================[ Perbandingan Weekday vs Weekend ]===================
weekday_rentals = filtered_day[filtered_day['weekday'] < 6]['cnt'].sum()
weekend_rentals = filtered_day[filtered_day['weekday'] >= 6]['cnt'].sum()

st.subheader("📌 Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan")
fig_bar = px.bar(
    x=["Hari Kerja", "Akhir Pekan"], 
    y=[weekday_rentals, weekend_rentals], 
    color=["Hari Kerja", "Akhir Pekan"],
    title="Perbandingan Penyewaan di Hari Kerja & Akhir Pekan",
    text_auto=True,
    color_discrete_sequence=["#FFA15A", "#AB63FA"]
)
st.plotly_chart(fig_bar)

# =====================[ Seasonal Rentals ]=======================
seasonal_rentals = filtered_day.groupby('season')['cnt'].sum().reset_index()
st.subheader("🍂 Penyewaan Berdasarkan Musim")
fig_season = px.bar(
    seasonal_rentals, x='season', y='cnt', 
    title="Penyewaan Sepeda Berdasarkan Musim",
    color_discrete_sequence=["#636EFA"]
)
st.plotly_chart(fig_season)

# =====================[ Weather Impact ]========================
weather_rentals = filtered_hour.groupby('weathersit')['cnt'].mean().reset_index()
st.subheader("🌤️ Pengaruh Cuaca Terhadap Penyewaan")
fig_weather = px.bar(
    weather_rentals, x='weathersit', y='cnt', 
    title="Rata-rata Penyewaan Berdasarkan Cuaca",
    color_discrete_sequence=["#00CC96"]
)
st.plotly_chart(fig_weather)

# =====================[ Kesimpulan & Rekomendasi ]========================
st.subheader("🎯 Kesimpulan & Rekomendasi")
st.markdown("""
✅ **Pola penyewaan sepeda menunjukkan tren berdasarkan waktu, musim, dan cuaca.**  
✅ **Cuaca sangat memengaruhi jumlah penyewaan, terutama saat kondisi ekstrem.**  
✅ **Manajemen armada dapat disesuaikan dengan waktu sibuk untuk efisiensi lebih tinggi.**  
✅ **Promosi bisa diarahkan ke periode penyewaan rendah untuk meningkatkan profitabilitas.**
""")

# =====================[ Footer ]========================
st.markdown("<br><hr><p style='text-align:center'>🚲 Created by <strong>Your Name</strong> | 2025</p>", unsafe_allow_html=True)
