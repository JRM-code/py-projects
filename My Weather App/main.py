import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

# --- CONFIG AND TITLES --- #
st.set_page_config(page_title='Weather App', page_icon=":cloud:", layout='wide')
st.sidebar.title(":cloud: City Weather")

def main():

    # --- SELECTBOX FOR LOCATION --- #
    loc_name = st.sidebar.text_input("Choose your location", placeholder="Enter a location").title()
    if not loc_name:
        loc_name = "Brisbane"
    else:
        loc_name = loc_name

    # --- GET LOCATION AND SEND LAT LON TO GET DATA -- #
    loc_url = f"http://api.openweathermap.org/geo/1.0/direct?q={loc_name}&limit=1&appid=???"

    def get_latlon(loc_url):
        response = requests.get(loc_url)
        loc_data = response.json()
        return loc_data
    
    loc_data = get_latlon(loc_url)
    lat = float(loc_data[0]["lat"])
    lon = float(loc_data[0]["lon"])

    # --- GET WEATHER DATA --- #
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["uv_index_max", "rain_sum"],
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "rain", "cloud_cover", "surface_pressure"], "timezone": "Australia/Brisbane",
    }
    headers = {
        "User-Agent": "MyWeatherApp/1.0 (example.com)"
    }

    def get_weather():
        response = requests.get(weather_url, params=params, headers=headers)
        weather_data = response.json()
        return weather_data
    
    weather_data = get_weather()

    # --- DISPLAY WEATHER DATA --- #
    # --- DISPLAY LOCATION AND LOCAL TIME --- #
    obj = TimezoneFinder()
    time_zone = obj.timezone_at(lng = lon, lat = lat)

    local_tz = pytz.timezone(time_zone)
    time_now = datetime.now(local_tz)

    format_string = "%B %d, %H:%M"

    st.metric(label="Location", value=loc_name, label_visibility="hidden")
    st.write(f"{time_now.strftime(format_string)}")

    # --- CREATE COLUMNS FOR DATA --- #
    col1, col2, col3 = st.columns(3, gap="small", border=True, width="stretch")

    with col1:
        st.subheader("Temp")
        st.image("img/temperature.jpg", width=100)
        temp = st.metric(label="Current Temp", value=f"{weather_data["current"]["temperature_2m"]} C")
        st.write("--------")
        temp_feel = st.metric(label="Feels Like", value=f"{weather_data["current"]["apparent_temperature"]} C", delta=round(weather_data["current"]["apparent_temperature"] - weather_data["current"]["temperature_2m"]))

    with col2:
        st.subheader("Humidity")
        st.image("img/humidity.jpg", width=100)
        humidity = st.metric(label="Current Humidity", value=f"{weather_data["current"]["relative_humidity_2m"]} %")
        st.write("--------")
        surface_pressure = st.metric(label="Surface Pressure", value=f"{weather_data["current"]["surface_pressure"]} hPa") 

    with col3:
        st.subheader("Wind")
        st.image("img/wind.jpg", width=100)
        wind = st.metric(label="Current Wind Speed", value=f"{weather_data["current"]["wind_speed_10m"]} km/h")
        gusts = st.metric(label="Wind Gusts", value=f"{weather_data["current"]["wind_gusts_10m"]} km/h") 
        wind_dir = weather_data["current"]["wind_direction_10m"]

    # --- Wind direction estimators, fix this --- # Rewrite with pythonic code. CS50p conditionals 32mins. 
        if wind_dir > 25 and wind_dir <= 45:
            st.metric(label="Wind Direction", value="NE")
        elif wind_dir > 45 and wind_dir <= 125:
            st.metric(label="Wind Direction", value="E")
        elif wind_dir > 125 and wind_dir <= 150:
            st.metric(label="Wind Direction", value="SE")
        elif wind_dir > 150 and wind_dir <= 210:
            st.metric(label="Wind Direction", value="S")
        elif wind_dir > 210 and wind_dir <= 250:
            st.metric(label="Wind Direction", value="SW")
        elif wind_dir > 250 and wind_dir <= 300:
            st.metric(label="Wind Direction", value="W")
        elif wind_dir > 300 and wind_dir <= 361 or wind_dir > 0 and wind_dir < 25:
            st.metric(label="Wind Direction", value="N")

    col4, col5 = st.columns(2, gap="small", border=True, width="stretch")

    with col4:
        # --- DISPLAY TEMPERATURE GRAPH FOR THE DAY --- #
        st.subheader("Temperature History")
        # --- CREATE TIME/TEMPERATURE DATAFRAME --- #
        df = pd.DataFrame({"Date/Time": weather_data["hourly"]["time"],"Temperature": weather_data["hourly"]["temperature_2m"],})

        # --- SELECT DATA BY DATE RANGE --- #
        start_date, end_date = st.select_slider("Use the date slider to select the data timeframe", options=df['Date/Time'], value=(df['Date/Time'][0], df['Date/Time'][18]), label_visibility='hidden')

        # --- CREATE DATA FRAME FOR DATE SELECTION --- #
        filt_data = df[(df['Date/Time'] >= start_date) & (df['Date/Time'] <= end_date)]

        # --- CREATE TEMPERATURE CHART --- #
        fig = px.line(filt_data, x="Date/Time", y="Temperature")

        # --- DISPLAY THE TEMPERATURE CHART --- #
        st.plotly_chart(fig, use_container_width=True)

    with col5:
            # --- DISPLAY UV INDEX FOR THE WEEK --- #
        st.subheader("UV Index")
        df2 = pd.DataFrame({"Date": weather_data["daily"]["time"],"UV Index": weather_data["daily"]["uv_index_max"],})
    
        # --- CREATE UV CHART --- #
        fig = px.line(df2, x="Date", y="UV Index")

        # --- DISPLAY THE UV CHART --- #
        st.plotly_chart(fig, use_container_width=True)

    # --- DISPLAY 7-DAY FORECAST --- #

    # --- DISPLAY CHANCE OF RAIN AND RAIN SINCE 9AM --- #

    # --- DISPLAY DESCRIPTION OF CONDITIONS --- #

if __name__ == '__main__':
    main()
