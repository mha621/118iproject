import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Be Active! Go Out and Explore!")
st.sidebar.markdown("# Be Active!")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
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

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("What are your activity goals today?") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))