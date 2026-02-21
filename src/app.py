import streamlit as st

st.title("Calorie Tracking App")

st.button("Log my meal")

uploaded_input = st.file_uploader("Upload an image of your meal", type=["jpg", "png"])

camera_input = st.camera_input("Take a picture of your meal")

if camera_input:
    st.image(camera_input)

if uploaded_input:
    st.image(uploaded_input)