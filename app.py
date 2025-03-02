import streamlit as st
import openai
import requests
from PIL import Image
import base64


import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DID_API_KEY = os.getenv("DID_API_KEY")
SUNO_API_KEY = os.getenv("SUNO_API_KEY")
dict


# Function to generate AI voice

def generate_voiceover(text, voice='alloy'):
    if not OPENAI_API_KEY:
        st.error("Missing OpenAI API Key! Add it in Streamlit Secrets Manager.")
        return None

    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": text,
        "voice": voice
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        audio_path = "generated_audio.mp3"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        return audio_path  # Return file path instead of raw content
    else:
        st.error(f"OpenAI API Error: {response.json()}")
        return None



# Function to generate talking AI character


def generate_talking_character(image_path, audio_url):
    if not DID_API_KEY:
        st.error("Missing D-ID API Key! Add it in Streamlit Secrets Manager.")
        return None

    url = "https://api.d-id.com/talks"
    headers = {"Authorization": f"Bearer {DID_API_KEY}"}
    data = {
        "source_url": image_path,
        "script": {
            "audio_url": audio_url
        }
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("result_url", "")
    else:
        st.error(f"D-ID API Error: {response.json()}")
        return None

# Function to create background music


def generate_background_music(mood='happy'):
    if not SUNO_API_KEY:
        st.error("Missing Suno API Key! Add it in Streamlit Secrets Manager.")
        return None

    url = "https://api.piapi.ai/suno/generate-music"  # Update this URL based on the chosen provider
    headers = {"Authorization": f"Bearer {SUNO_API_KEY}"}
    data = {"mood": mood}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("music_url", "")
    else:
        st.error(f"Suno API Error: {response.json()}")
        return None

# Streamlit UI
st.title("AI Talking Character Video Creator")

uploaded_file = st.file_uploader("Upload Character Image", type=["jpg", "png"])
script = st.text_area("Enter your script")


voice_option = st.selectbox("Select Voice Type", ["nova", "shimmer", "echo", "onyx", "fable", "alloy", "ash", "sage", "coral"])

music_mood = st.selectbox("Select Background Music Mood", ["happy", "calm", "energetic"])

if st.button("Generate Video"):
    if uploaded_file and script:
        image_path = f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.read()).decode()}"
        audio_url = generate_voiceover(script, voice_option)
        video_url = generate_talking_character(image_path, audio_url)
        music_url = generate_background_music(music_mood)
        
        st.video(video_url)
        st.audio(music_url, format='audio/mp3')
    else:
        st.error("Please upload an image and enter a script.")


