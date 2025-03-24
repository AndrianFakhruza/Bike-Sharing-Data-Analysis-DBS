import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Menentukan path file
base_path = os.path.dirname(os.path.abspath(__file__))
day_path = os.path.join(base_path, "day.csv")
hour_path = os.path.join(base_path, "hour.csv")

# Fungsi untuk membaca dataset
def load_data():
    try:
        df_day = pd.read_csv(day_path)
        df_hour = pd.read_csv(hour_path)
        return df_day, df_hour
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Memuat data
df_day, df_hour = load_data()

if df_day is not None and df_hour is not None:
    st.title("📊 Bike Sharing Dashboard")
    st.sidebar.header("Filter Data")
    
    # Pilih jenis data yang ingin ditampilkan
    dataset_option = st.sidebar.radio("Pilih Dataset", ("Per Hari", "Per Jam"))
    df = df_day if dataset_option == "Per Hari" else df_hour
    
    # Pilih musim
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df['season_name'] = df['season'].map(season_mapping)
    selected_season = st.sidebar.selectbox("Pilih Musim", df['season_name'].unique())
    df_filtered = df[df['season_name'] == selected_season]
    
    # Tampilkan data
    st.subheader(f"Dataset - {dataset_option} ({selected_season})")
    st.dataframe(df_filtered.head())
    
    # Visualisasi jumlah penyewaan sepeda per musim
    st.subheader("🚴‍♂️ Jumlah Penyewaan Sepeda per Musim")
    fig = px.bar(df_day, x='season_name', y='cnt', title="Total Penyewaan Sepeda per Musim",
                 labels={'cnt': 'Jumlah Penyewaan', 'season_name': 'Musim'})
    st.plotly_chart(fig)
    
    # Pengaruh kecepatan angin terhadap jumlah penyewaan
    st.subheader("🌬️ Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
    fig2 = px.scatter(df_hour, x='windspeed', y='cnt', title="Hubungan Kecepatan Angin & Penyewaan",
                      labels={'windspeed': 'Kecepatan Angin', 'cnt': 'Jumlah Penyewaan'},
                      trendline="ols")
    st.plotly_chart(fig2)
    
    # Tambahan insight bisa ditambahkan di sini
    
else:
    st.error("Data tidak tersedia. Pastikan file CSV sudah ada di folder yang benar.")
