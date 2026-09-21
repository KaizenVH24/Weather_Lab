import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).parent / "src"))

from weatherlab.services.weather_service import WeatherService
from weatherlab.utils.weather_codes import (
    get_weather_description,
    get_weather_icon,
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="WeatherLab",
    page_icon="🌦️",
    layout="wide",
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .weather-card {
        padding: 1.5rem;
        border-radius: 1rem;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 1rem;
    }

    .temperature {
        font-size: 3.5rem;
        font-weight: 700;
    }

    .weather-icon {
        font-size: 4rem;
    }

    .forecast-card {
        padding: 1rem;
        border-radius: 1rem;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.15);
        text-align: center;
        min-height: 180px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("WeatherLab")

st.caption(
    "A Python weather dashboard powered by Open-Meteo"
)


# --------------------------------------------------
# Search
# --------------------------------------------------

city = st.text_input(
    "Search for a city",
    placeholder="Try Nashik, Mumbai, London...",
)


# --------------------------------------------------
# Cached API request
# --------------------------------------------------

@st.cache_data(ttl=600)
def fetch_weather(city_name: str):
    service = WeatherService()
    return service.get_weather(city_name)


# --------------------------------------------------
# Main application
# --------------------------------------------------

if city:

    with st.spinner("Fetching weather data..."):

        try:
            report = fetch_weather(city)

        except ValueError as error:
            st.error(str(error))
            st.stop()

        except Exception as error:
            st.error(
                "Something went wrong while fetching weather data."
            )
            st.stop()

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    location = report.location
    current = report.current

    st.subheader(
        f"{location.name}, {location.country}"
    )

    st.caption(
        f"Timezone: {location.timezone}  |  "
        f"Coordinates: "
        f"{location.latitude:.2f}, "
        f"{location.longitude:.2f}"
    )

    # --------------------------------------------------
    # Current weather
    # --------------------------------------------------

    icon = get_weather_icon(current.weather_code)

    description = get_weather_description(
        current.weather_code
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Temperature",
            f"{current.temperature:.1f}°C",
        )

    with col2:
        st.metric(
            "Humidity",
            f"{current.humidity:.0f}%",
        )

    with col3:
        st.metric(
            "Wind",
            f"{current.wind_speed:.1f} km/h",
        )

    with col4:
        st.metric(
            "Precipitation",
            f"{current.precipitation:.1f} mm",
        )

    st.markdown(
        f"""
        <div class="weather-card">

        <span class="weather-icon">{icon}</span>

        <div class="temperature">
            {current.temperature:.1f}°C
        </div>

        <h3>{description}</h3>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # Hourly forecast
    # --------------------------------------------------

    st.divider()

    st.subheader("Hourly Forecast")

    hourly_df = pd.DataFrame(
        [
            {
                "Time": item.time,
                "Temperature": item.temperature,
                "Rain Probability": (
                    item.precipitation_probability
                ),
            }
            for item in report.hourly[:24]
        ]
    )

    if not hourly_df.empty:

        fig = px.line(
            hourly_df,
            x="Time",
            y="Temperature",
            markers=True,
            labels={
                "Temperature": "Temperature (°C)",
                "Time": "Time",
            },
            title="Next 24 Hours",
        )

        fig.update_layout(
            hovermode="x unified",
            height=400,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Rain probability
    # --------------------------------------------------

    if not hourly_df.empty:

        rain_fig = px.bar(
            hourly_df,
            x="Time",
            y="Rain Probability",
            labels={
                "Rain Probability": "Probability (%)",
                "Time": "Time",
            },
            title="Rain Probability — Next 24 Hours",
        )

        rain_fig.update_layout(
            height=350,
        )

        st.plotly_chart(
            rain_fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # 7-day forecast
    # --------------------------------------------------

    st.divider()

    st.subheader("7-Day Forecast")

    forecast_columns = st.columns(
        len(report.daily)
    )

    for column, forecast in zip(
        forecast_columns,
        report.daily,
    ):

        icon = get_weather_icon(
            forecast.weather_code
        )

        description = get_weather_description(
            forecast.weather_code
        )

        with column:

            st.markdown(
                f"""
                <div class="forecast-card">

                <h4>
                    {forecast.date.strftime("%a")}
                </h4>

                <div class="weather-icon">
                    {icon}
                </div>

                <strong>
                    {forecast.temperature_max:.0f}°C
                </strong>

                <span>
                    / {forecast.temperature_min:.0f}°C
                </span>

                <p>
                    {description}
                </p>

                <small>
                    Rain: {forecast.precipitation_probability:.0f}%
                </small>

                </div>
                """,
                unsafe_allow_html=True,
            )