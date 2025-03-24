import os
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# =========================[ Load Dataset ]=========================
base_path = os.path.dirname(os.path.abspath(__file__))
file_day = os.path.join(base_path, "day.csv")

if os.path.exists(file_day):
    df_day = pd.read_csv(file_day)
    st.success("✅ Data berhasil dimuat!")
else:
    st.error("❌ Error: File day.csv tidak ditemukan! Periksa kembali path-nya.")
    st.stop()

# =====================[ Sidebar - Filter Tahun ]=====================
st.sidebar.header("🔍 Filter Data")
year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + sorted(df_day['yr'].unique().tolist()))

filtered_day = df_day.copy()
if year != "Semua":
    filtered_day = filtered_day[filtered_day['yr'] == year]

# =====================[ Pola Penggunaan Sepeda Berdasarkan Musim ]=======================
st.subheader("🍂 Pola Penyewaan Sepeda Berdasarkan Musim")

season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_day['season_label'] = filtered_day['season'].map(season_labels)

season_rentals = filtered_day.groupby('season_label')['cnt'].mean().reset_index()

fig_season = px.bar(
    season_rentals, x='season_label', y='cnt', 
    title="Rata-rata Penyewaan Sepeda Berdasarkan Musim",
    color_discrete_sequence=["#FFA15A"]
)
st.plotly_chart(fig_season)

st.markdown("""
📌 **Insight**  
- **Musim mana yang memiliki penyewaan terbanyak?**  
- **Apakah musim dingin cenderung lebih rendah dibandingkan musim panas?**  
""")

# =====================[ Pengaruh Kecepatan Angin terhadap Penyewaan ]=======================
st.subheader("🌬️ Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")

fig_wind = px.scatter(
    filtered_day, x='windspeed', y='cnt', 
    trendline="ols",
    title="Hubungan Kecepatan Angin dan Penyewaan Sepeda",
    color_discrete_sequence=["#00CC96"]
)
st.plotly_chart(fig_wind)

st.markdown("""
📌 **Insight**  
- **Apakah ada hubungan negatif antara kecepatan angin dan jumlah penyewaan?**  
- **Apakah kecepatan angin tinggi mengurangi jumlah penyewaan secara signifikan?**  
""")

# =====================[ Kesimpulan & Rekomendasi ]========================
st.subheader("🎯 Kesimpulan & Rekomendasi")
st.markdown("""
✅ **Pola musiman menunjukkan bahwa penyewaan sepeda lebih banyak di musim tertentu.**  
✅ **Kecepatan angin dapat memengaruhi penyewaan, terutama saat angin lebih kencang.**  
✅ **Manajemen penyewaan bisa mempertimbangkan promosi atau diskon di musim yang lebih sepi.**  
""")
