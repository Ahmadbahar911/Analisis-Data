import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data df_hour
#df_hour = pd.read_csv("..\dashboard\hour.csv")
df_hour = pd.read_csv("dashboard/hour.csv")
df_hour.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']

for i in df_hour.columns:
  if i in drop_col:
    df_hour.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
df_hour.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
df_hour['month'] = df_hour['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

df_hour['weekday'] = df_hour['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_hour['weather_cond'] = df_hour['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

df_hour['season'] = df_hour['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat kolom baru 'rentang_waktu' berdasarkan jam
def assign_time_of_day(hr):
    if 6 <= hr < 12:
        return 'Pagi'
    elif 12 <= hr < 16:
        return 'Siang'
    elif 16 <= hr < 20:
        return 'Sore'
    else:
        return 'Malam'

# Asign jam ke kategori rentang waktu
df_hour['rentang_waktu'] = df_hour['hr'].apply(assign_time_of_day)

# Hitung jumlah penyewaan berdasarkan rentang waktu
#grouped = df_hour.groupby('rentang_waktu')['count'].sum().reset_index()

# Menyiapkan rentang_waktu_df
def create_rentang_waktu_df(df):
    rentang_waktu_df = df.groupby(by='rentang_waktu').agg({
        'count': 'sum'
    }).reset_index()
    return rentang_waktu_df



# Membuat komponen filter
min_date = pd.to_datetime(df_hour['dateday']).dt.date.min()
max_date = pd.to_datetime(df_hour['dateday']).dt.date.max()
 
with st.sidebar:
    image_url = "https://drive.google.com/uc?id=1CTiCok6hqQJXJVWLbInf_ZWKAMm_aO-K"
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    st.image(img)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df_hour[(df_hour['dateday'] >= str(start_date)) & 
                (df_hour['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
rentang_waktu_df = create_rentang_waktu_df(main_df)


# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Rental Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Penyewaan Harian')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Pengguna Biasa', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Jumlah Pengguna', value= daily_rent_total)

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Penyewaan Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(16, 8))


sns.barplot(
    x='season',
    #x=season_rent_df.index,
    y=season_rent_df['count'],
    data=season_rent_df,
    palette='viridis',
    ax=ax
)

for index, row in enumerate(season_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Musim')
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Penyewaan Berdasarkan Cuaca')

fig, ax = plt.subplots(figsize=(16, 8))


sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette='viridis',
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Tren Penyewaan Sepeda Berdasarkan Bulan di Tahun Pertama dan Kedua
# Tampilkan subheader
st.subheader('Tren Penyewaan Sepeda Berdasarkan Bulan di Tahun Pertama dan Kedua')

# Membuat data agregat untuk tren penyewaan per bulan di setiap tahun
monthly_trend = df_hour.groupby(['year', 'month'])['count'].sum().reset_index()

# Menentukan urutan bulan (dari Januari hingga Desember)
month_order = ['Jan', 'Feb', 'Mar', 'April', 'Apr', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Mengatur kolom 'month' sebagai kategori dengan urutan yang benar
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=month_order, ordered=True)

# Visualisasi dengan line plot menggunakan Matplotlib dan Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=monthly_trend,
    x='month',
    y='count',
    hue='year',
    palette=['blue', 'red'],  # Warna garis
    ax=ax
)

# Menyesuaikan legend agar sesuai dengan garis
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=['Tahun Pertama', 'Tahun Kedua'], title='Tahun')

# Menambahkan judul dan label
ax.set_title('Tren Penyewaan Sepeda Berdasarkan Bulan di Tahun Pertama dan Kedua')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan (cnt)')

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Tren Jumlah Penyewaan Sepeda Berdasarkan Rentang Waktu
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Rentang Waktu')

fig, ax = plt.subplots(figsize=(16, 8))


sns.barplot(
    x='rentang_waktu',
    y=rentang_waktu_df['count'],
    data=rentang_waktu_df,
    palette='viridis',
    ax=ax
)

for index, row in enumerate(rentang_waktu_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)



ax.set_xlabel('Rentang Waktu')
ax.set_ylabel('Jumlah Penyewaan (cnt)')
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


st.caption('Copyright (c) Ahmad Bahar 2024')
