# streamlit run main.py
import os
import streamlit as st
import google.generativeai as genai

try:
    ai_name = os.getenv("BOT_INFO", "ยูริ")
    bot_info = f"คุณชื่อ {ai_name}"

    genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

    AI_NAME = os.getenv("AI_NAME", "ยูริอิอิ")
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
    instruction = f"""
    {bot_info} คุณให้ความช่วยเหลือทางด้านต่างๆเป็นอย่างดีและตอบคำถามโดยคำนึงถึงวัฒนธรรมของประเทศไทย ไม่ลามกจนเกินไป ไม่เกี่ยวข้องด้านศาสนา การชี้นำต่างๆ และตอบคำถามเป็นภาษาไทยเป็นส่วนใหญ่
    """
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        system_instruction=instruction,
    )

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    st.title("ยูริ")

    st.chat_message("assistant").markdown(
        "สวัสดีค่ะ ยูริอยู่ที่นี่เพื่อช่วยเหลือคุณ มีอะไรให้ยูริช่วยเหลือไหมคะ?"
    )

    def role_to_streamlit(role: str) -> str:
        if role == "model":
            return "assistant"
        else:
            return role

    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("ใส่ข้อความของคุณ..."):
        st.chat_message("user").markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
except Exception as e:
    st.error(f"An error occurred: {e}")
