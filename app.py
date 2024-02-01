# Aim of this project is when an user uploads an image, and they can
# ask a question from the image and the model will come up with a response.

#importing libraries
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

#configuring API key
genai.configure(api_key=os.getenv('API_KEY'))

#
def get_response(uploaded_image, user_question):
    """
    this method takes an image and and user asked question and returns the response
    :param uploaded_image: user uploaded image
    :param user_question: user asked question
    :return: response from the model
    """
    if uploaded_image and user_question:
        model = genai.GenerativeModel('gemini-pro-vision') # using gemini-pro-vision model
        response = model.generate_content([user_question, uploaded_image[0]]) # getting response from model
        return response # returning the response

def reformat_image(uploaded_image):
    """
    this method reformats the image uploaded by the user to the model's understandable format
    :param uploaded_image: use uploaded image
    :return: returns the image after changing the format
    """
    if uploaded_image:
        image_bytes = [
            {
                'mime_type': uploaded_image.type,
                'data': uploaded_image.getvalue()
            }
        ]
        return image_bytes
    else: # when no file is uploaded
        raise FileNotFoundError('No file uploaded')

#streamlit
st.set_page_config(page_title='Image_Interpreter-GenAI') #title
st.header('Image Interpreter') #header
uploaded_image = st.file_uploader('Upload image', type=['jpeg', 'jpg', 'png']) #user uploaded image
#displaying user uploaded image on the web page
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, use_column_width=True)

user_question = st.text_input('ask question from image') #user question
submit = st.button('Ask') #button

if submit: # if button is clicked
    user_image = reformat_image(uploaded_image) # call reformat_image method and get return value
    response = get_response(user_image, user_question) # call get_response method and get return value
    st.header('Response') # header
    st.write(response.text) # writing response on web page