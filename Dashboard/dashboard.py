import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Data
def load_data():
    base_path = os.path.dirname(__file__)  # Ambil direktori file ini
    day_path = os.path.join(base_path, "day.csv")

    try:
        day_df = pd.read_csv(day_path)

        # Ubah tipe data tanggal
        if "dteday" in day_df.columns:
            day_df["dteday"] = pd.to_datetime(day_df["dteday"])
        else:
            st.error("Kolom 'dteday' tidak ditemukan dalam 'day.csv'.")

        return day_df

    except FileNotFoundError as e:
        st.error(f"❌ File tidak ditemukan: {e}")
        return None

day_df = load_data()

if day_df is not None:
    # Sidebar Menu dengan Dropdown
    st.sidebar.title("📊 Menu Analisis")
    menu = st.sidebar.selectbox(
        "Pilih Analisis:", 
        ["Pola Penggunaan Sepeda Berdasarkan Musim", "Pengaruh Kecepatan Angin terhadap Penyewaan"]
    )

    # Header Dashboard
    st.title("🚲 Dashboard Penyewaan Sepeda")
    st.write("Analisis penggunaan sepeda berdasarkan musim dan pengaruh kecepatan angin.")

    # 1️⃣ Pola Penggunaan Sepeda Berdasarkan Musim
    if menu == "Pola Penggunaan Sepeda Berdasarkan Musim":
        st.header("📌 Pola Penggunaan Sepeda Berdasarkan Musim")
        if "season" in day_df.columns and "cnt" in day_df.columns:
            season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
            day_df["season_label"] = day_df["season"].map(season_mapping)

            season_count = day_df.groupby("season_label")["cnt"].sum().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x="season_label", y="cnt", data=season_count, ax=ax, palette="coolwarm")
            ax.set_xlabel("Musim")
            ax.set_ylabel("Jumlah Penyewaan")
            ax.set_title("Pola Penggunaan Sepeda Berdasarkan Musim")
            st.pyplot(fig)

            # Insight
            max_season = season_count.loc[season_count["cnt"].idxmax(), "season_label"]
            st.success(f"✅ Hasil: Jumlah penyewaan sepeda tertinggi terjadi pada {max_season}.")
        else:
            st.error("❌ Kolom 'season' atau 'cnt' tidak ditemukan di 'day.csv'.")

    # 2️⃣ Pengaruh Kecepatan Angin terhadap Penyewaan
    elif menu == "Pengaruh Kecepatan Angin terhadap Penyewaan":
        st.header("📌 Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
        if "windspeed" in day_df.columns and "cnt" in day_df.columns:
            fig, ax = plt.subplots()
            sns.scatterplot(x="windspeed", y="cnt", data=day_df, alpha=0.5)
            ax.set_xlabel("Kecepatan Angin")
            ax.set_ylabel("Jumlah Penyewaan")
            ax.set_title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
            st.pyplot(fig)

            st.success("✅ Hasil: Secara umum, kecepatan angin yang lebih tinggi cenderung berhubungan dengan penurunan jumlah penyewaan sepeda.")
        else:
            st.error("❌ Kolom 'windspeed' atau 'cnt' tidak ditemukan di 'day.csv'.")
