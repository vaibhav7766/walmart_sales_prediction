import streamlit as st
from numpy import array
from sklearn.ensemble import RandomForestRegressor
import pickle as pk
import base64

def load_rfr_model(model_path):
    try:
        with open(model_path, "rb") as file:
            model = pk.load(file)
        return model
    except Exception as e:
        st.write("Error loading the model:", str(e))
        return None

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    backdrop-filter: blur(1000px);
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(r"pxfuel (3).jpg")

st.markdown("----")

st.title("Walmart Sales Prediction")

model_path = r"rfr_model.pkl"
rfr_model = load_rfr_model(model_path)

if rfr_model is not None:
    store = st.number_input("Enter store number: ",value = 0)
    Fuel_Price = st.number_input("Enter fuel price: ",)
    CPI = st.number_input("Enter CPI: ")
    Unemployment = st.number_input("Enter unemployment: ")
    Day = st.number_input("Enter day: ",value = 0,max_value = 31)
    Month = st.number_input("Enter month: ",value = 0,max_value = 12)
    Year = st.number_input("Enter year: ",value = 0)
    holiday_flag = st.number_input("Is it a holiday?(0 for no, 1 for yes): ",min_value = 0,max_value = 1)

    if st.button("Predict"):
        input_data = array([[store, Fuel_Price, CPI, Unemployment, Day, Month, Year, holiday_flag]])
        prediction = rfr_model.predict(input_data)

        st.write(f"Predicted Sales for that day: {prediction[0]:.2f}")
else:
    st.write("Model failed to load. Please check the model file path.")
