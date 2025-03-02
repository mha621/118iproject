import os
import openai
import streamlit as st
from PIL import Image
import requests
from openai import OpenAI
from pathlib import Path

st.markdown("# Envision Your Ideal City 📷")
st.sidebar.markdown("# Imagine the Future!")

st.write("Paint the picture of your ideal urban landscape! You have two options to help our app create a visual rendering of your ideal future cityscape. You can either select a feature from the dropdown menu or describe the features you envision in your dream city, from vibrant pedestrian-friendly streets to green spaces and community hubs. Whether you choose from the menu or write your own description, your input will guide the creation of an image that represents your ideal city.")
st.write("")
st.write("**Notice of Consent:** By submitting a description, you agree to share it with our AI model for image generation. The image will be used solely for the purpose of creating a visual representation of your ideal city and will not be stored or shared with third parties.")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def download_image(filename, url):
  response = requests.get(url)
  if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
  else:
        print("Error downloading image from URL:", url)

def filename_from_input(prompt):
   # Remove all non-alphanumeric characters from the prompt except spaces.
    alphanum = ""
    for character in prompt:
        if character.isalnum() or character == " ":
            alphanum += character
    # Split the alphanumeric prompt into words.
    # Take the first three words if there are more than three. Else, take all    of them.
    alphanumSplit = alphanum.split()
    if len(alphanumSplit) > 3:
        alphanumSplit = alphanumSplit[:3]
    # Join the words with underscores and return the result.
    return "images/" + " ".join(alphanumSplit)


# Create an image
# If model is not specified, the default is DALL-E-2.
def get_image(prompt, model="dall-e-3"):
    image = client.images.generate(
        prompt=prompt,
        model=model,
        n=1,
        size="1024x1024"
    )
    # Download the image

    filename = str(Path(__file__).resolve().parent)+ "/"+ filename_from_input(prompt) + ".png"
    download_image(filename, image.data[0].url)

    return image


#print(response)
st.write("*"*40)

# Create a dropdown menu

features = ['expanded and improved sidewalks', 'more bike lanes', 'more green spaces like parks, gardens, trees, and flowers', 'better lighting in streets to improve safety', 'pedestrian streets, plazas, and courtyards to prioritize pedestrians over vehicles']

st.write("If you cannot think of any ideas about what you would like in your ideal city, feel free to choose from the dropdown menu below!")

selected_feature = st.selectbox('Select a feature you would like to see more of in your city:', features)

# Display the selected feature
# st.write(f"You selected: {selected_feature}")


with st.form(key = "chat1"):
    # Include the selected feature in the prompt
    prompt = f"In my ideal city, I would like to have {selected_feature.lower()}."
    st.text_input('**What features would you like to see in your ideal city?**"', value=prompt)
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = get_image(prompt)
        image = Image.open(str(Path(__file__).parent)+'/'+filename_from_input(prompt)+'.png')
        st.image(image, caption='New Image')


st.write("")
st.write("*"*40)

# ...
st.write("Otherwise, if you know what you have an idea of what you would like in your ideal city, feel free to type it in the text box below!")
st.write("When describing your ideal city, try to be as specific as possible. For example, you could say 'I would like a city with lots of green spaces, bike lanes, and pedestrian-friendly streets. I would also like to have a park with a lake and a playground.' The more specific you are, the better the AI will be able to generate an image that matches your description.")

with st.form(key = "chat2"):
    prompt = st.text_input('**In your ideal city, what are some key features you would like to have?\
                           For example, you could say "I would like to have a park with a lake and a playground.**"')
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        response = get_image(prompt)
        image = Image.open(str(Path(__file__).parent)+'/'+filename_from_input(prompt)+'.png')
        st.image(image, caption='New Image')