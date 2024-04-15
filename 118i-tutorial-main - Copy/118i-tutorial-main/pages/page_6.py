#implement the page 6 that we talked about in the chat for reading a pdf'''
# we are using fitz or PyMuPDF'''
#import PyMuPDF
import fitz
import streamlit as st
import os
import openai
from openai import OpenAI
from pathlib import Path
openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def main():
    st.title("Submit a PDF to Analyze Walking Pain Points in San Jose!")

    def get_summary(text):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content
    
    def get_key_points(text):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and extract the key points."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content

    def get_action_items(text):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content
    
    def get_sentiment(transcription):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible. Please keep it to fewer than 5 sentences."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message.content
    # Create a file uploader
    uploaded_file = st.file_uploader("Choose a PDF file related to the issue of limited walkability in San Jose that you want to analyze. You will receive a summary, key points, action items, and a sentiment analysis of this PDF.", type="pdf")

    if uploaded_file is not None:
        # Load the PDF
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        # Concatenate the text from all pages
        full_text = ""
        for i in range(len(pdf)):
            page = pdf.load_page(i)
            full_text += page.get_text("text")
        
        # Analyze the full text
        st.markdown("## Summary of the entire PDF:")
        
        summary = get_summary(full_text)
        st.markdown(f"**Summary:**\n{summary}")

        key_points = get_key_points(full_text)
        st.markdown("## Key Points of the entire PDF:") 
        st.markdown(f"**Key Points:**\n{key_points}")

        action_items = get_action_items(full_text)
        st.markdown("## Action Items of the entire PDF:")
        st.markdown(f"**Action Items:**\n{action_items}")

        sentiment = get_sentiment(full_text)
        st.markdown("## Sentiment of the entire PDF:")
        st.markdown(f"**Sentiment:**\n{sentiment}")

        with open(r"C:\Users\Michelle\Downloads\118i\118iproject\118i-tutorial-main - Copy\118i-tutorial-main\pages\results.txt", "w") as f:
            f.write("Summary:\n")
            f.write(summary)
            f.write("\n\nKey Points:\n")
            f.write(key_points)
            f.write("\n\nAction Items:\n")
            f.write(action_items)
            f.write("\n\nSentiment:\n")
            f.write(sentiment)


if __name__ == "__main__":
    main()

    
