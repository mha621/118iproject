import os
import openai
import streamlit as st
from PIL import Image
import requests
from openai import OpenAI
from pathlib import Path

st.markdown("# How do you want to fix up your city?")
st.sidebar.markdown("# Picture Your Ideal City")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def get_completion(prompt, model="gpt-4-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "You are the chatbot component of an app called Walk-E that is focused\
            on making cities more walkable. Your job is to interact with users and encourage\
                them to walk to places. You can suggest walking challenges to users, such as walking\
                    10,000 steps or walking a mile. Walk-E is also connected with local businesses\
                        and can point users towards these mom-and-pop shops to increase foot traffic\
                            while encouraging people to walk more. You also provide people who take up these walking challenges\
                            with rewards such as $2 off coupons for these businesses."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png', 'jpeg', 'pdf', 'txt'])
if uploaded_file is not None:
    # Assuming it's an image for now
    # Process the file here, e.g., display it
    st.image(uploaded_file.read(), caption='Uploaded Image', use_column_width=True)

    user_input = st.text_input("Ask me a question or type a command:")
if st.button("Submit"):
    response = get_completion(user_input)
    st.write(response)