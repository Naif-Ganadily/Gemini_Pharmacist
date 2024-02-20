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
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    with st.form(key='chat_form'):
        chat_input = st.text_input("Ask me anything about the medicine you are prescribed by your doctor...", key="chat_input")
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        st.session_state.chat_history.append(f"You: {chat_input}")
        
        # Construct the input prompt for the model
        input_prompt = f"""
        Analyze the uploaded image of the medicine and answer the specific question: "{chat_input}" Provide information that is precise, relevant, and understandable for non-medical users.
        """

        # Get the model response
        response = get_gemini_response(input_prompt, image_data)
        
        # Add model response to chat history
        st.session_state.chat_history.append(f"AI Pharmacist: {response}")
        
        # Reset the input box by clearing the session state for the next query
        st.session_state.chat_input = ""

    # Display chat history
    for chat in st.session_state.chat_history:
        st.text(chat)

# Initializing the App (Front end setup)

st.set_page_config(page_title="AI Pharmacist", page_icon="💊", layout="centered", initial_sidebar_state="auto")

st.header("AI Pharmacist")
uploaded_file = st.file_uploader("Upload an image of your Medicine", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    image_data = input_image_setup(uploaded_file)
    
    # Trigger chat interface after image upload with the ability to converse
    chat_interface(image_data)