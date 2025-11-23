import streamlit as st
import requests

# --- CONFIG AND TITLES --- #
st.set_page_config(page_title='Weather App', layout='wide')
st.title("Weather App")
st.sidebar.title("Location & Forecast")

# --- GET LOCATION AND SEND LAT LON TO GET DATA -- #
# The dictionary of places with latitude and longitude
PLACES = {
    "Brisbane": {"lat": -27.47, "lon": 153.02},
    "Sydney": {"lat": -33.8688, "lon": 151.2093},
    "Melbourne": {"lat": -37.81, "lon": 144.96},
    "Adelaide": {"lat": -34.93, "lon": 138.60},
    "Darwin": {"lat": -12.46, "lon": 130.84},
    "Perth": {"lat": -31.95, "lon": 115.86},
    "Hobart": {"lat": -42.88, "lon": 147.33},
    "Canberra": {"lat": -35.28, "lon": 149.13}
}

# --- SELECTBOX FOR LOCATION --- #
place_name = st.sidebar.selectbox("Choose your location", options=PLACES)


def lat_lon():
    return PLACES.keys()
lat_lon()

def get_coords(place_name):
    coords = PLACES.get(place_name, {})
    #st.write(coords)
    return coords 
coords = get_coords(place_name)

# --- GET DATA --- #
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": coords["lat"],
	"longitude": coords["lon"],
	"hourly": "temperature_2m","current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "pressure_msl", "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m", "rain", "is_day"],
	"timezone": "Australia/Brisbane"
}
headers = {
    "User-Agent": "MyWeatherApp/1.0 (example.com)"
}

def get_weather():
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data
data = get_weather()

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