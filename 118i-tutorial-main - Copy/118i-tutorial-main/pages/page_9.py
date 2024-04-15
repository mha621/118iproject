from google.cloud import vision
import io
import streamlit as st
from PIL import Image

# Create a Vision client
client = vision.ImageAnnotatorClient()

from google.oauth2 import service_account
from google.cloud import vision

# Specify the path to your service account key
# credentials = service_account.Credentials.from_service_account_file('/path/to/your/service-account-file.json')

# client = vision.ImageAnnotatorClient(credentials=credentials)

def analyze_image(image_file):
    # Convert the image file to bytes
    image_bytes = image_file.read()
    image = vision.Image(content=image_bytes)

    # Use Google Cloud Vision to detect labels in the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Get the description of each label
    descriptions = [label.description for label in labels]

    return descriptions

uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png', 'jpeg'])
if uploaded_file is not None:
    # Display the image
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    # Analyze the image
    descriptions = analyze_image(uploaded_file)
    st.write("Image contains:", descriptions)