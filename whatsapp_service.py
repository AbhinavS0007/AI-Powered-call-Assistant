import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp(message: str):
    print("Sending WhatsApp message...")
    print("From:", os.getenv("TWILIO_WHATSAPP_FROM"))
    print("To:", os.getenv("YOUR_WHATSAPP"))

    twilio_client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),
        to=os.getenv("YOUR_WHATSAPP")
    )

    print("WhatsApp message sent!")
