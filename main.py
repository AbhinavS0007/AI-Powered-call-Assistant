from fastapi import FastAPI, Request
from fastapi.responses import Response
import requests
import os
from dotenv import load_dotenv

from whisper_service import transcribe_audio
from gemini_service import generate_reply, summarize_conversation
from whatsapp_service import send_whatsapp

# Load environment variables
load_dotenv()

app = FastAPI()

# Conversation memory
conversation_log = []

# Safety limit
MAX_TURNS = 12


@app.get("/")
def home():
    return {"message": "AI assistant running"}


# Incoming call
@app.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call():
    response = """
    <Response>
        <Say>Hello, this is Abhinav's AI assistant. How can I help you?</Say>
        <Record action="/process-recording" maxLength="20" />
    </Response>
    """
    return Response(content=response, media_type="application/xml")


# Process recording
@app.api_route("/process-recording", methods=["GET", "POST"])
async def process_recording(request: Request):
    try:
        form_data = await request.form()
        recording_url = form_data.get("RecordingUrl")

        print("Recording URL:", recording_url)

        # Download audio
        audio_file = requests.get(
            recording_url + ".wav",
            auth=(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )
        )

        with open("call.wav", "wb") as f:
            f.write(audio_file.content)

        # Transcribe
        caller_text = transcribe_audio("call.wav")
        print("Caller said:", caller_text)

        conversation_log.append(f"Caller: {caller_text}")

        # Generate AI reply
        ai_reply = generate_reply(conversation_log, caller_text)
        print("AI reply:", ai_reply)

        conversation_log.append(f"Assistant: {ai_reply}")

        # Detect end phrases
        end_phrases = [
            "goodbye",
            "thank you for calling",
            "have a nice day",
            "bye"
        ]

        should_end = any(phrase in ai_reply.lower() for phrase in end_phrases)

        if len(conversation_log) >= MAX_TURNS:
            should_end = True

        # End call and summarize
        if should_end:
            summary = summarize_conversation(conversation_log)
            print("Call Summary:", summary)

            send_whatsapp(f"Call Summary:\n{summary}")

            conversation_log.clear()

            twiml = f"""
            <Response>
                <Say>{ai_reply}</Say>
                <Hangup/>
            </Response>
            """
        else:
            # Continue conversation
            twiml = f"""
            <Response>
                <Say>{ai_reply}</Say>
                <Record action="/process-recording" maxLength="20" />
            </Response>
            """

        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        print("ERROR during call processing:", str(e))

        # Always return valid TwiML
        error_twiml = """
        <Response>
            <Say>Sorry, something went wrong. Please try again later.</Say>
            <Hangup/>
        </Response>
        """
        return Response(content=error_twiml, media_type="application/xml")
