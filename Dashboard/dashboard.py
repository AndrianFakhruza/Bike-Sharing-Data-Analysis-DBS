import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Mapping untuk season dan cuaca agar lebih jelas
season_map = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat"}

# Menentukan path file
base_path = os.path.dirname(os.path.abspath(__file__))  
day_file = os.path.join(base_path, "day.csv")  
hour_file = os.path.join(base_path, "hour.csv")  

# Pilihan dataset
data_option = st.sidebar.radio("Pilih Dataset", ["Per Hari", "Per Jam"])

if data_option == "Per Hari":
    df = pd.read_csv(day_file)
else:
    df = pd.read_csv(hour_file)

# Pastikan season dan weathersit diubah ke kategori yang lebih deskriptif
df["season"] = df["season"].map(season_map)
df["weathersit"] = df["weathersit"].map(weather_map)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + df["season"].dropna().unique().tolist())
weather = st.sidebar.selectbox("Pilih Cuaca", ["Semua"] + df["weathersit"].dropna().unique().tolist())

# Apply filters
filtered_df = df.copy()
if season != "Semua":
    filtered_df = filtered_df[filtered_df['season'] == season]
if weather != "Semua":
    filtered_df = filtered_df[filtered_df['weathersit'] == weather]

# Main Dashboard Title
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("Analisis data penyewaan sepeda berdasarkan faktor musim, cuaca, dan waktu.")

# Key Metrics
total_rentals = filtered_df['cnt'].sum()
daily_avg = round(filtered_df['cnt'].mean(), 2)
max_rental = filtered_df['cnt'].max()
min_rental = filtered_df['cnt'].min()

st.subheader("📊 Metrik Utama")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Rata-rata", f"{daily_avg:,}")
col3.metric("Penyewaan Tertinggi", f"{max_rental:,}")
col4.metric("Penyewaan Terendah", f"{min_rental:,}")

# Seasonal Rentals
seasonal_rentals = filtered_df.groupby('season')['cnt'].sum().reset_index()
st.subheader("🍂 Penyewaan Berdasarkan Musim")
fig_season = px.bar(seasonal_rentals, x='season', y='cnt', title="Penyewaan Berdasarkan Musim", color='season')
st.plotly_chart(fig_season)

# Weather impact
weather_rentals = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
st.subheader("🌤️ Pengaruh Cuaca Terhadap Penyewaan")
fig_weather = px.bar(weather_rentals, x='weathersit', y='cnt', title="Rata-rata Penyewaan Berdasarkan Cuaca", color='weathersit')
st.plotly_chart(fig_weather)

st.subheader("🎯 Kesimpulan dan Rekomendasi")
st.markdown("""
- Pola penyewaan sepeda dipengaruhi oleh musim dan cuaca.
- Penyewaan tertinggi terjadi pada kondisi cuaca tertentu.
- Manajemen armada dapat disesuaikan untuk efisiensi lebih tinggi.
""")
