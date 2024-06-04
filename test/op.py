import streamlit as st
import cv2
import base64
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv

# OpenAI API Key



def encode_image(pil_image):
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def send_to_openai(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "extract the text in the image as it is without any additions"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    if "choices" in response_data:
            content = response_data["choices"][0]["message"]["content"]
            usage = response_data.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            cost_per_token = 0.00002  # Example cost per token
            total_cost = total_tokens * cost_per_token
            return content, total_cost
    else:
            return "No text extracted from the image.", 0


# # Streamlit app
# st.title("Learning app")

# # Button for uploading an image
# image_source = st.selectbox("Image Source", ["Upload Image", "Capture from Camera"],index=None)
# if image_source == "Upload Image":
#     uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption='Uploaded Image')
#         base64_image = encode_image(image)
#         text, cost = send_to_openai(base64_image)
        
#         # Display the extracted text and the total cost
#         st.text_area("Extracted Text", value=text, height=300)
#         st.write(f"Total Cost: ${cost:.5f}")

# elif image_source == "Capture from Camera":
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if ret:
#         st.image(frame, caption='Camera Preview')

# # Button for capturing the image
#     if st.button("Capture Image"):
#     # Capture the image
#         ret, frame = cap.read()
#         if ret:
#             st.image(frame, caption='Captured Image')
#             base64_image = encode_image(frame)
#             response_data = send_to_openai(base64_image)
#             text, cost = send_to_openai(base64_image)
#             st.write(response_data)
#     cap.release()
