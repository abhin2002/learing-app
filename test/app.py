import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ui import set_image_dpi, enhance_image, extract_text, capture_image
from op import encode_image, send_to_openai
from backend import handle_factual_query

st.title("Learning APP")
image_source = st.selectbox("Image Source", ["Upload Image", "Capture from Camera"])

if image_source == "Upload Image":
    img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = cv2.imdecode(np.frombuffer(img_file_buffer.read(), np.uint8), 1)
        image = set_image_dpi(image, dpi=300)
        enhanced_image = enhance_image(image)
        text = extract_text(enhanced_image)
        st.image(image, caption="Original Image")
        st.text_area("Extracted Text", value=text, height=300)

        if st.button("Conform and Continue", key="confirm_upload"):
            st.success("Text saved successfully!")
            question = text  # Assume extracted text is the question
            answer = handle_factual_query(question)
            st.text_area("Answer", value=answer, height=300)
            with open("extracted_text.txt", "w") as file:
                file.write(text)

        if st.button("Retry the Analysis", key="retry_upload"):
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            base64_image = encode_image(pil_image)
            new_text, cost = send_to_openai(base64_image)
            st.text_area("New Extracted Text", value=new_text, height=300)
            st.write(f"Analysis Cost: ${cost:.5f}")

elif image_source == "Capture from Camera":
    if st.button("Capture Image"):
        captured_image = capture_image()
        if captured_image is not None:
            enhanced_image = enhance_image(captured_image)
            text = extract_text(enhanced_image)
            st.image(captured_image, caption="Captured Image")
            st.text_area("Extracted Text", value=text, height=300)

            if st.button("Conform and Continue", key="confirm_capture"):
                question = text  # Assume extracted text is the question
                answer = handle_factual_query(question)
                st.text_area("Answer", value=answer, height=300)
                with open("extracted_text.txt", "w") as file:
                    file.write(text)
                st.success("Text saved successfully!")

            if st.button("Retry the Analysis", key="retry_capture"):
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                base64_image = encode_image(pil_image)
                new_text, cost = send_to_openai(base64_image)
                st.text_area("New Extracted Text", value=new_text, height=300)
                st.write(f"Analysis Cost: ${cost:.5f}")

                if st.button("Conform and Continue"):
                    question = text  # Assume extracted text is the question
                    answer = handle_factual_query(question)
                    st.text_area("Answer", value=answer, height=300)
                    with open("extracted_text.txt", "w") as file:
                        file.write(text)
                    st.success("Text saved successfully!")
