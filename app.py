import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent / "src"))

from weatherlab.services.weather_service import WeatherService


st.set_page_config(
    page_title="WeatherLab",
    page_icon="🌦️",
    layout="wide",
)


st.title("🌦️ WeatherLab")
st.caption("A weather dashboard built with Python and Open-Meteo")


city = st.text_input(
    "Search for a city",
    placeholder="e.g. Nashik, Mumbai, London...",
)


if city:

    with st.spinner("Fetching weather data..."):

        try:
            service = WeatherService()

            report = service.get_weather(city)

            st.success(
                f"{report.location.name}, "
                f"{report.location.country}"
            )

            current = report.current

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Temperature",
                    f"{current.temperature}{current.temperature_unit}",
                )

            with col2:
                st.metric(
                    "Humidity",
                    f"{current.humidity}%",
                )

            with col3:
                st.metric(
                    "Wind",
                    f"{current.wind_speed} km/h",
                )

            with col4:
                st.metric(
                    "Precipitation",
                    f"{current.precipitation} mm",
                )

            st.divider()

            st.subheader("7-Day Forecast")

            for forecast in report.daily:
                st.write(
                    f"**{forecast.date.strftime('%A, %d %B')}**  "
                    f"{forecast.temperature_min}°C → "
                    f"{forecast.temperature_max}°C"
                )

        except ValueError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "Something went wrong while fetching weather data."
            )