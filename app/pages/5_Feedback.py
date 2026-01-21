import smtplib  # module whichi is using Simple Mail Transfer Protocol , standard for sending emails ( connect with the server, login, sending emails)
from pathlib import Path
import os
from dotenv import load_dotenv

import streamlit as st
from email.message import EmailMessage
import ssl

from src.session_init import init_session_state

init_session_state()


GMAIL_TOKEN_PATH = Path(__file__).parent.parent / "src" / ".env"
load_dotenv(GMAIL_TOKEN_PATH)
GMAIL_TOKEN = os.getenv("gmail_app_token")


st.title("Feedback form")
st.markdown(
    "I will appreciate any type of feedback, what you like and what could be improved"
)


Sender_Email = "feedback.project.pm@gmail.com"
Receiver_Email = "damian.piotr.gasior@gmail.com"


feedback = st.text_area("Type your message below: ", "Example text", height=200)


st.markdown(
    """The below information will be helpful for me to understand, who is viewing this dashboard
    Data is anonymous. Your email is not stored. Only the below parameters and message.
    """
)

sender_type = st.radio(
    "Choose your profile:",
    ["recruiter", "private investor", "other employee", "other"],
    index=3,
)


source = st.radio(
    "How did you get tothis page:",
    ["linkedin", "other social media", "recomendation from a friend", "other"],
    index=0,
)


email = EmailMessage()
email["From"] = Sender_Email
email["To"] = Receiver_Email
email["Subject"] = "Feedback_service_financial_dashboard"
email.set_content(
    f"""{feedback} 
Users profile : {sender_type}
Users_source : {source}

"""
)

context = (
    ssl.create_default_context()
)  # it veryfies the certificate from gmail if it the one from root CA, checks the domain smtp.gmail.com, cert expiry date, if yes a key is created


def send_message():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(Sender_Email, GMAIL_TOKEN)
        server.send_message(email)


st.markdown("Once you are ready with the feedback , please  hit **Send message**")


if st.button("Send message"):
    send_message()
