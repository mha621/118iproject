import streamlit as st
from openai import OpenAI
from PIL import Image
import openai
import os
import base64
import requests

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png', 'jpeg'])
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

    payload = {
  "model": "gpt-4-turbo",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
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

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

st.write(response.json()['choices'][0]['message']['content'])