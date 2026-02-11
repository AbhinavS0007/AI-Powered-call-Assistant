from gemini_service import generate_reply, summarize_conversation
from whatsapp_service import send_whatsapp

# Fake conversation memory
conversation_log = []


def test_full_pipeline():
    print("Starting full pipeline test...\n")

    # Simulate 5 conversation turns
    for turn in range(5):
        caller_text = input(f"Caller message {turn+1}: ").strip()

        if not caller_text:
            print("Empty input detected. Ending conversation.")
            break

        print("Caller said:", caller_text)
        conversation_log.append(f"Caller: {caller_text}")

        # Generate AI reply
        print("Generating AI reply...")
        ai_reply = generate_reply(conversation_log, caller_text)
        print("AI reply:", ai_reply)

        conversation_log.append(f"Assistant: {ai_reply}")
        print("-" * 40)

    # Generate summary
    print("\nGenerating summary...")
    summary = summarize_conversation(conversation_log)
    print("Summary:", summary)

    # Send WhatsApp
    send_whatsapp(f"Pipeline Test Summary:\n{summary}")
    print("Pipeline test completed.")


if __name__ == "__main__":
    test_full_pipeline()
