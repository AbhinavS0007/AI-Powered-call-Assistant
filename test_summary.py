from gemini_service import summarize_conversation
from whatsapp_service import send_whatsapp

def test_whatsapp_summary():
    # Fake conversation
    conversation_log = [
        "Caller: Hello, I’m calling about the internship position.",
        "Assistant: Sure, may I know your name?",
        "Caller: My name is Rahul.",
        "Assistant: Thank you Rahul. What role are you applying for?",
        "Caller: Backend developer role.",
        "Assistant: Got it. I will inform Abhinav about your interest."
    ]

    print("Testing summary generation...")

    # Generate summary
    summary = summarize_conversation(conversation_log)

    print("Summary:", summary)

    # Send WhatsApp message
    send_whatsapp(f"Test Call Summary:\n{summary}")

    print("WhatsApp message sent!")


if __name__ == "__main__":
    test_whatsapp_summary()
