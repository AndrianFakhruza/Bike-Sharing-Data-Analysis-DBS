import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Data
def load_data():
    base_path = os.path.dirname(__file__)  # Ambil direktori file ini
    day_path = os.path.join(base_path, "day.csv")
    hour_path = os.path.join(base_path, "hour.csv")

    try:
        day_df = pd.read_csv(day_path)
        hour_df = pd.read_csv(hour_path)

        # Ubah tipe data
        if "dteday" in day_df.columns:
            day_df["dteday"] = pd.to_datetime(day_df["dteday"])
        else:
            st.error("Kolom 'dteday' tidak ditemukan dalam 'day.csv'.")

        return day_df, hour_df

    except FileNotFoundError as e:
        st.error(f"❌ File tidak ditemukan: {e}")
        return None, None

day_df, hour_df = load_data()

if day_df is not None and hour_df is not None:
    # Sidebar Menu dengan Dropdown
    st.sidebar.title("📊 Menu Analisis")
    menu = st.sidebar.selectbox(
        "Pilih Analisis:", 
        ["Statistik Penyewaan", "Penyewaan Berdasarkan Jam", "Weekday vs Weekend", "Pengaruh Suhu"]
    )

    # Header Dashboard
    st.title("🚲 Dashboard Penyewaan Sepeda")
    st.write("Analisis data penyewaan sepeda berdasarkan berbagai faktor.")

    # Statistik Penyewaan
    if menu == "Statistik Penyewaan":
        st.header("📌 Statistik Penyewaan Sepeda")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Penyewaan", "3,292,679")
        col2.metric("Rata-rata Penyewaan per Hari", "4,504")
        col3.metric("Penyewaan Tertinggi", "8,714 pada 15 Sep 2012")

    # Jumlah Penyewaan Berdasarkan Jam
    elif menu == "Penyewaan Berdasarkan Jam":
        st.header("📌 Jumlah Penyewaan Berdasarkan Jam")
        if "hr" in hour_df.columns and "cnt" in hour_df.columns:
            hourly_count = hour_df.groupby("hr")["cnt"].sum().reset_index()
            fig, ax = plt.subplots()
            sns.lineplot(x="hr", y="cnt", data=hourly_count, marker="o", ax=ax)
            ax.set_xlabel("Jam")
            ax.set_ylabel("Jumlah Penyewaan")
            ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Jam")
            st.pyplot(fig)
        else:
            st.error("❌ Kolom 'hr' atau 'cnt' tidak ditemukan di 'hour.csv'.")

    # Analisis Weekday vs Weekend
    elif menu == "Weekday vs Weekend":
        st.header("📌 Penyewaan pada Hari Kerja vs Akhir Pekan")
        if "weekday" in day_df.columns and "cnt" in day_df.columns:
            weekday_total = day_df[day_df['weekday'] < 5]['cnt'].sum()
            weekend_total = day_df[day_df['weekday'] >= 5]['cnt'].sum()
            st.bar_chart(pd.DataFrame({"Weekday": [weekday_total], "Weekend": [weekend_total]}))
            st.success(f"✅ Hasil: Jumlah penyewaan lebih tinggi pada hari kerja ({weekday_total}) dibandingkan akhir pekan ({weekend_total}).")
        else:
            st.error("❌ Kolom 'weekday' atau 'cnt' tidak ditemukan di 'day.csv'.")

    # Pengaruh Suhu terhadap Penyewaan
    elif menu == "Pengaruh Suhu":
        st.header("📌 Pengaruh Suhu terhadap Penyewaan")
        if "temp" in day_df.columns and "cnt" in day_df.columns:
            fig, ax = plt.subplots()
            sns.scatterplot(x="temp", y="cnt", data=day_df, alpha=0.5)
            ax.set_xlabel("Suhu")
            ax.set_ylabel("Jumlah Penyewaan")
            ax.set_title("Pengaruh Suhu terhadap Penyewaan Sepeda")
            st.pyplot(fig)
            st.success("✅ Hasil: Semakin tinggi suhu, jumlah penyewaan cenderung meningkat.")
        else:
            st.error("❌ Kolom 'temp' atau 'cnt' tidak ditemukan di 'day.csv'.")
