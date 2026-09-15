import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Penguin Species Predictor",
    page_icon="🐧",
)

st.title("🐧 Penguin Species Predictor")

st.write(
    "Enter the penguin characteristics below and the model "
    "will predict its species."
)

island = st.selectbox(
    "Island",
    ["Biscoe", "Dream", "Torgersen"],
)

bill_length_mm = st.number_input(
    "Bill length (mm)",
    min_value=1.0,
    value=46.5,
)

bill_depth_mm = st.number_input(
    "Bill depth (mm)",
    min_value=1.0,
    value=17.9,
)

flipper_length_mm = st.number_input(
    "Flipper length (mm)",
    min_value=1.0,
    value=192.0,
)

body_mass_g = st.number_input(
    "Body mass (g)",
    min_value=1.0,
    value=3500.0,
)

sex = st.selectbox(
    "Sex",
    ["FEMALE", "MALE"],
)


if st.button("Predict species"):
    input_data = {
        "island": island,
        "bill_length_mm": bill_length_mm,
        "bill_depth_mm": bill_depth_mm,
        "flipper_length_mm": flipper_length_mm,
        "body_mass_g": body_mass_g,
        "sex": sex,
    }

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=input_data,
            timeout=10,
        )

        response.raise_for_status()

        result = response.json()

        st.success(
            f"Predicted species: {result['prediction']}"
        )

        st.subheader("Prediction probabilities")

        for species, probability in result["probabilities"].items():
            st.write(
                f"{species}: {probability * 100:.2f}%"
            )

    except requests.RequestException as error:
        st.error(
            f"Could not connect to the prediction API: {error}"
        )