import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv
from fpdf import FPDF
import tempfile
load_dotenv() # Load all the environment variables
from PIL import Image


# This Doesn't Change:
# --------------------------------------------
load_dotenv() # Load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(image_data):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(image_data)
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_pairs = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_pairs
    else:
        raise FileNotFoundError("No File Uploaded")
# --------------------------------------------
    

# Initializing the App (Front end setup)
st.set_page_config(page_title="AI Pharmacist", page_icon="💊", layout="centered", initial_sidebar_state="auto")
st.header("AI Pharmacist")

# Initialize session state for messages and image data
if "messages" not in st.session_state:
    st.session_state.messages = []

# Image upload interface
uploaded_file = st.file_uploader("Upload an image of your Medicine", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.session_state.image_data = input_image_setup(uploaded_file)

# Display chat messages from history
for message in st.session_state.messages:
    role = "You" if message["role"] == "user" else "AI"
    st.text(f"{role}: {message['content']}")

# Chat input
if "chat_reset" not in st.session_state:
    st.session_state.chat_reset = False

if not st.session_state.chat_reset:
    user_input = st.text_input("Ask me anything about the medicine...", key="user_query")
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if "image_data" in st.session_state and st.session_state.image_data:
            # Get AI's response based on the uploaded image
            ai_response = get_gemini_response(st.session_state.image_data)
        else:
            ai_response = "Please upload an image of the medicine for a detailed analysis."
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Optionally, add a button to clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_reset = True
    st.rerun()

# Reset chat_reset state after rerun
st.session_state.chat_reset = False