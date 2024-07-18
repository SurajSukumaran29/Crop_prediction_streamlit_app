import streamlit as st
import pickle
from PIL import Image
import base64


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    set_background('dark-gradient-sim9nt3zt5rtx5oo.jpg')  # Replace with your image file path

    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state.page = "About"

    st.sidebar.title("Navigation")
    about_button = st.sidebar.button("About")
    prediction_button = st.sidebar.button("Prediction")

    if about_button:
        st.session_state.page = "About"
    if prediction_button:
        st.session_state.page = "Prediction"

    if st.session_state.page == "About":
        st.title("About the App")
        st.markdown("""
        ### CROP PREDICTION
        This application predicts the best crop to plant based on various soil and weather conditions. 
        The prediction model is built using machine learning techniques and considers the following factors:
        - Nitrogen level in the soil
        - Phosphorus level in the soil
        - Potassium level in the soil
        - Temperature
        - Humidity
        - pH value of the soil
        - Rainfall

        ### How to use the app
        1. Go to the Prediction page.
        2. Enter the values for the above factors.
        3. Click on the 'PREDICT' button to get the recommended crop.
        """)
    elif st.session_state.page == "Prediction":
        st.title("CROP PREDICTION")
        #image = Image.open("crops.jpg")
        #st.image(image, width=800)

        model = pickle.load(open('crop_prediction1.sav', 'rb'))
        scaler = pickle.load(open('minmaxscaler.sav', 'rb'))

        Nitr = st.text_input("Nitrogen", placeholder="Between 0 - 140")
        phos = st.text_input("Phosphorus", placeholder="Between 5 - 145")
        Pota = st.text_input("Potassium", placeholder="Between 5 - 205")
        temp = st.text_input("Temperature", placeholder="Between 8.8 - 43.7")
        Hum = st.text_input("Humidity", placeholder="Between 14.2 - 99.9")
        ph = st.text_input("pH Value", placeholder="Between 3.5 - 9.9")
        Rain = st.text_input("Rainfall", placeholder="Between 20.2 - 298.4")

        pred = st.button('PREDICT')

        if pred:
            try:
                inputs = [float(Nitr), float(phos), float(Pota), float(temp), float(Hum), float(ph), float(Rain)]
                scaled_inputs = scaler.transform([inputs])
                prediction = model.predict(scaled_inputs)
                st.markdown(f"<h2 style='text-align: center; color: white;'>Recommended Crop: {prediction[0]}</h2>",
                            unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter valid numeric values for all inputs.")


if __name__ == "__main__":
    main()
