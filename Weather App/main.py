import streamlit as st
import requests

# --- CONFIG AND TITLES --- #
st.set_page_config(page_title='Weather App', layout='wide')
st.title("Weather App")
st.sidebar.title("Location & Forecast")

# --- GET DATA --- #
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 27.47,
	"longitude": 153.02,
	"hourly": "temperature_2m","current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "pressure_msl", "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m"],
	"timezone": "Australia/Brisbane"
}
headers = {
    "User-Agent": "MyWeatherApp/1.0 (example.com)"
}

def get_weather() -> str:
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data
data = get_weather()

# --- SELECTBOX FOR LOCATION --- #
location = st.sidebar.selectbox("Choose your location", options=['Brisbane', 'New York'])

# --- SELECTBOX FOR FORECAST TIMEFRAME --- #
st.sidebar.selectbox("Choose your forecast", options=['Today', '3-Days', '5-Days', '7-Days'])

# --- DISPLAY HIGH AND LOW TEMPS --- #
# --- DISPLAY HUMIDITY --- #
col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top", border=True, width="stretch")

with col1:
    st.subheader("Temp")
    st.image("img/temperature.jpg")
    st.write((data["current"]["temperature_2m"]))
    st.write("Feels Like")
    st.write((data)["current"]["apparent_temperature"])

with col2:
    st.subheader("Humidity")
    st.image("img/humidity.jpg")
    st.write((data["current"]["relative_humidity_2m"]))
    st.write("Sea Level Pressure")
    st.write((data)["current"]["pressure_msl"])

with col3:
    st.subheader("Wind")
    st.image("img/wind.jpg")
    st.write((data["current"]["wind_speed_10m"]))
    st.write("Gusting")
    st.write((data)["current"]["wind_gusts_10m"])

    st.write((data["current_units"]["wind_speed_10m"]))

# --- DISPLAY CHANCE OF RAIN AND RAIN SINCE 9AM --- #

# --- DISPLAY DESCRIPTION OF CONDITIONS --- #