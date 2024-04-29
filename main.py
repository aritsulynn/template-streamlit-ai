# streamlit run main.py
import os
import streamlit as st
import google.generativeai as genai

try:
    AI_NAME = os.getenv("AI_NAME", "AI")
    genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        system_instruction=os.getenv("INSTRUCTION", ""),
    )

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    st.title(AI_NAME)

    st.chat_message("assistant").markdown(
        f"Hello! I'm {AI_NAME}. How can I help you today?"
    )

    def role_to_streamlit(role: str) -> str:
        if role == "model":
            return "assistant"
        else:
            return role

    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("message AI..."):
        st.chat_message("user").markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
except Exception as e:
    st.error(f"An error occurred: {e}")
