import cloudinary
import streamlit as st

cloudinary.config(
    cloud_name=st.secrets["CLOUD NAME"],
    api_key=st.secrets["969647552977694"],
    api_secret=st.secrets["J_zSuHl3aWgzT-0A1XaMsP4AvycT"]
)
