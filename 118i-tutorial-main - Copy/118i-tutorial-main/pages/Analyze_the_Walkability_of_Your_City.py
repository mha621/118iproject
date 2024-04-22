import streamlit as st
from openai import OpenAI
from PIL import Image
import openai
import os
import base64
import requests

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

st.markdown("# How Walkable is Your City? 📊")
st.sidebar.markdown("# Analyze the Walkability of Your City")

st.write("")
st.write("Capture the essence of your city to uncover potential barriers to walkability. Share an image to shed light on areas that may hinder pedestrian-friendly experiences in San Jose.")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

uploaded_file = st.file_uploader("**Submit an Image of Your City Below:**", type=['jpg', 'png', 'jpeg'])
if uploaded_file is not None:
    # Convert the file to an image
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Save the image to the "images" folder
    image_path = os.path.join(script_dir, "images", uploaded_file.name)
    uploaded_image.save(image_path)

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    # Create a placeholder for the status message
    status_message = st.empty()
    status_message.write("Analyzing the image...")

    payload = {
      "model": "gpt-4-turbo",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "What’s in this image? How can it contribute to the level of walkability in a city? What can be done to improve these features in the photo to make a city more pedestrian friendly?"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json=payload)

    st.write(response.json()['choices'][0]['message']['content'])