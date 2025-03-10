import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Ubah tipe data
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Header Dashboard
st.title("🚲 Dashboard Penyewaan Sepeda")
st.write("Analisis data penyewaan sepeda berdasarkan berbagai faktor.")

# Statistik Penyewaan
st.header("Total Penyewaan")
st.subheader("3,292,679")

st.header("Rata-rata Penyewaan per Hari")
st.subheader("4,504")

st.header("Penyewaan Tertinggi")
st.subheader("8,714 pada 15 Sep 2012")

# Jumlah Penyewaan Berdasarkan Jam
st.header("Jumlah Penyewaan Berdasarkan Jam")
hourly_count = hour_df.groupby("hr")["cnt"].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(x="hr", y="cnt", data=hourly_count, marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Jam")
st.pyplot(fig)

# Analisis Weekday vs Weekend
st.header("📌 Bagaimana tren jumlah penyewaan sepeda berdasarkan hari kerja dan akhir pekan?")
weekday_total = day_df[day_df['weekday'] < 5]['cnt'].sum()
weekend_total = day_df[day_df['weekday'] >= 5]['cnt'].sum()
st.bar_chart(pd.DataFrame({"Weekday": [weekday_total], "Weekend": [weekend_total]}))
st.success(f"✅ Hasil: Jumlah penyewaan sepeda lebih tinggi pada hari kerja ({weekday_total}) dibandingkan akhir pekan ({weekend_total}).")

# Pengaruh Suhu terhadap Penyewaan
st.header("📌 Bagaimana pengaruh suhu terhadap jumlah penyewaan sepeda?")
fig, ax = plt.subplots()
sns.scatterplot(x="temp", y="cnt", data=day_df, alpha=0.5)
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda")
st.pyplot(fig)
st.success("✅ Hasil: Dari grafik terlihat bahwa semakin tinggi suhu, jumlah penyewaan cenderung meningkat. Hal ini menunjukkan bahwa orang lebih sering menyewa sepeda saat cuaca lebih hangat.")
