import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

names = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']

raw_df = pd.read_csv('/dashboard/main_data.csv')

def get_df(city):
    df = raw_df[raw_df['station'] == city]
    
    return df

def get_day_night_data(main_df):
    observe = main_df.groupby(by=['year', 'month', 'day', 'hour']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean'
    }).reset_index()

    observe['time_of_day'] = observe['hour'].apply(
        lambda x: 'day' if 6 <= x <= 18 else 'night')

    day_night_data = observe.groupby('time_of_day').agg({
        'PM2.5': 'mean',
        'PM10': 'mean'
    }).reset_index()
    
    return day_night_data

main_df = get_df('Aotizhongxin')

with st.sidebar:
    city = st.selectbox("Pilih Kota", names)
    main_df = get_df(city)

    # date = st.date_input("Select Observation Date", )
    
st.title(city)
col1, col2, col3 = st.columns(3)
colb1, colb2 = st.columns(2)

recent = main_df.iloc[-1]
with col1:
    quality = recent['PM2.5']
    
    if quality <= 50:
        aq = "Good"
    elif 51 <= quality <= 150:
        aq = "Moderate"
    else:
        aq = "Bad"
    
    st.metric("Air Quality", aq)

with col2:
    temperature = recent['TEMP']
    st.metric("Temperature", str(temperature) + " °C")

with col3:
    wind_diredction = recent['wd']
    st.metric("Wind Direction", wind_diredction)
    
with colb1:
    curah_hujan = recent['RAIN']
    st.metric("Curah Hujan", curah_hujan)
    
with colb2:
    titik_embun = recent['DEWP']
    st.metric("Titik Embun", str(titik_embun) + " °C")

aq_graph = main_df.groupby(by='date').agg({
    'PM2.5': 'mean',
    'PM10': 'mean'
}).reset_index().iloc[-100:]

st.header("Kualitas Udara 100 Hari Terakhir")
st.line_chart(aq_graph, x='date', y='PM10')

day_night_comparison = get_day_night_data(main_df)

st.header("Perbandingan Kualitas Udara pada Siang dan Malam")
st.bar_chart(day_night_comparison.set_index('time_of_day'))

pollutant = ['NO2', 'O3', 'SO2']

st.header("Kandungan Pollutan Pada Data")
st.bar_chart(recent[pollutant])