import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Where would you like to explore?")
st.sidebar.markdown("# Go find new places!")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

import requests

def get_food_places(location):
    api_key = 'yelp_api_key_placeholder'
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {'term': 'food', 'location': location}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['businesses']
    else:
        return None

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
                            with rewards such as $2 off coupons for these businesses. Keep in mind that \
                                your suggestions come from the Yelp API and these suggestions to users\
                                    can be restaurants, shops, or other businesses."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.form(key = "chat"):
    prompt = st.text_input("Enter your message:")
    submitted = st.form_submit_button("Send")

    if submitted and prompt:
        response = get_completion(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # If the user's message contains the word 'place', get food places
        if 'place' in prompt.lower():
            location = st.text_input("Enter your location:")
            food_places = get_food_places(location)
            if food_places:
                st.write("Here are some food places you can walk to:")
                for place in food_places:
                    st.write(place['name'])
            # else:
                # st.write("Sorry, I couldn't find any food places in your location.")