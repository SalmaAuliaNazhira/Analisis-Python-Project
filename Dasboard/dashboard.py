import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set(style='whitegrid')

# Load dataset
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_working_day_df(df):
    working_day_df = df.groupby(by="workingday").agg({"cnt": "count"}).rename(index={0: "Hari Libur", 1: "Hari Kerja"})
    return working_day_df

def create_weather_df(df):
    weather_df = df.groupby(by="weathersit").agg({"cnt": "count"}).rename(index={1: "Cerah", 2: "Berawan", 3: "Hujan", 4: "Hujan Lebat"})
    return weather_df

def create_hourly_usage_df(df):
    hourly_usage_df = df.groupby(by="hr").agg({"cnt": "sum"}).sort_values(by="cnt", ascending=False)
    return hourly_usage_df

# Sidebar 
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Waktu',
    min_value=day_df["dteday"].min().date(),
    max_value=day_df["dteday"].max().date(),
    value=[day_df["dteday"].min().date(), day_df["dteday"].max().date()]
    
)

# Filter dataset 
filtered_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) &
                     (day_df["dteday"] <= pd.to_datetime(end_date))]

st.sidebar.header("User Feedback")
user_name = st.sidebar.text_input("Masukkan Nama Anda:")
feedback = st.sidebar.text_area("Berikan Feedback Anda:")
today_date = datetime.date.today()
st.sidebar.write(f"Tanggal Hari Ini: {today_date}")

# judul Streamlit 
st.title("🚴‍♂️ Bike Sharing Dashboard")
st.write("Analisis pola penggunaan sepeda berdasarkan hari kerja, cuaca, dan waktu.")

# Menyiapkan dataframes
working_day_df = create_working_day_df(filtered_df)
weather_df = create_weather_df(filtered_df)
filtered_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) &
                            (hour_df["dteday"] <= pd.to_datetime(end_date))]
hourly_usage_df = create_hourly_usage_df(filtered_hour_df)

# 1. Perbandingan Penggunaan Sepeda pada Hari Kerja vs Hari Libur
st.subheader("Penggunaan Sepeda: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#808080", "#008080"]
working_day_df["cnt"].plot(kind="bar", color=colors, ax=ax)
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.set_xticklabels(working_day_df.index, rotation=0)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Insight
- Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur.
- Menunjukkan bahwa banyak pengguna sepeda adalah pekerja atau pelajar yang menggunakannya untuk perjalanan sehari-hari.
        """
    )

# 2. Pengaruh Cuaca terhadap Penggunaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#008080", "#808080", "#808080", "#808080"]
weather_df["cnt"].plot(kind="bar", color=colors, ax=ax)
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.set_xticklabels(weather_df.index, rotation=0)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Insight
- Penggunaan sepeda tertinggi terjadi saat cuaca cerah, kemudian menurun saat cuaca berawan dan semakin turun saat hujan.
- Saat hujan lebat, jumlah pengguna sepeda turun drastis, menunjukkan bahwa cuaca buruk sangat memengaruhi keputusan pengguna untuk bersepeda.
        """
    )

# 3. Pola Penggunaan Sepeda Berdasarkan Jam
st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=hourly_usage_df.index, y=hourly_usage_df["cnt"], palette="viridis", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Insight
- Puncak penggunaan terjadi pada jam 17:00 (5 sore), kemungkinan karena jam pulang kerja.
- Jam 8 pagi juga tinggi, mungkin akibat perjalanan ke kantor/sekolah.
- Penggunaan sangat rendah antara jam 0:00 - 5:00, kemungkinan karena malam hari.
        """
    )
    
# Footer
st.caption("© 2025 Salma Aulia Nazhira")
