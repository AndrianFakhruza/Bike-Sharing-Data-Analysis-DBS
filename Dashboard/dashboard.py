import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Load dataset
df = pd.read_csv("day.csv")

# Mapping season labels
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df["season"] = df["season"].map(season_labels)

# 1. Pola penggunaan sepeda berdasarkan musim
plt.figure(figsize=(8, 5))
sns.barplot(x=df["season"], y=df["cnt"], palette="coolwarm")
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Pola Penggunaan Sepeda Berdasarkan Musim")
plt.show()

# 2. Pengaruh kecepatan angin terhadap jumlah penyewaan sepeda
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["windspeed"], y=df["cnt"], alpha=0.5)
plt.xlabel("Kecepatan Angin")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Hubungan Kecepatan Angin dan Penyewaan Sepeda")
plt.show()

# Menghitung korelasi antara windspeed dan jumlah penyewaan
corr, _ = pearsonr(df["windspeed"], df["cnt"])
print(f"Korelasi antara kecepatan angin dan jumlah penyewaan sepeda: {corr:.2f}")
