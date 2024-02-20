import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv
load_dotenv() # Load all the environment variables
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Backend setup

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()  # Read the file as bytes

        image_pairs = [
            {
                "mime_type": uploaded_file.type,  # image/jpeg
                "data": bytes_data
            }
        ]
        return image_pairs
    else:
        raise FileNotFoundError("No File Uploaded")

# Chat Functionality

def chat_interface(image_data):
    st.session_state.chat_history = st.session_state.get('chat_history', [])
    chat_input = st.text_input("Ask me anything about the medicine you are prescribed by your doctor...", key="chat_input")
    submit_button = st.button(label="Submit")

    if submit_button and chat_input:
        user_query = chat_input
        st.session_state.chat_history.append(f"You: {user_query}")

        # Dynamically construct the input prompt based on the user query
        input_prompt = f"""
        Analyze the uploaded image of the medicine and answer the specific question: "{user_query}" Provide information that is precise, relevant, and understandable for non-medical users.
        """

        response = get_gemini_response(input_prompt, image_data)
        st.session_state.chat_history.append(f"AI Pharmacist: {response}")

        # Display chat history
        for chat in st.session_state.chat_history:
            st.text(chat)

        # Clear the input box for the next query by resetting the state
        st.session_state.chat_input = ""

# Initializing the Streamlit App (Front end setup)

st.set_page_config(page_title="AI Pharmacist", page_icon="💊", layout="centered", initial_sidebar_state="auto")

st.header("AI Pharmacist")
uploaded_file = st.file_uploader("Upload an image of your Medicine", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    image_data = input_image_setup(uploaded_file)
    
    # Trigger chat interface after image upload with the ability to converse
    chat_interface(image_data)