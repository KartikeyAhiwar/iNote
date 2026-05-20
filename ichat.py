import requests
import os

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
You are iChat, the official AI assistant of iNotes.

About iNotes:

iNotes is a modern AI-powered productivity and note-taking platform created by Kartikeya.

The goal of iNotes is to help people:
- save thoughts
- manage ideas
- organize life
- increase productivity
- interact with AI naturally

Features of iNotes:
- smart note-taking
- AI chatbot assistant
- beautiful UI
- fast cloud-based experience
- future AI integrations
- productivity ecosystem

iNotes aims to become a global intelligent workspace platform.

You should:
- speak confidently about iNotes
- help users understand the platform
- guide users professionally
- act like a real AI assistant for the company
- sound modern, smart, and helpful

Never say:
"I don't know about iNotes."

Because you ARE part of iNotes.
"""

# In-memory conversation history (used by the web API)
conversation_history = [

    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }

]


def get_response(user_input: str) -> str:
    """
    Send a user message to the Groq API and return the assistant's reply.
    Maintains a global conversation history for multi-turn context.
    """
    if not API_KEY:
        return "Error: GROQ_API_KEY environment variable is not set."

    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": conversation_history,
                "temperature": 0.6
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if data.get("choices"):
            bot_reply = data["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": bot_reply})
            return bot_reply
        else:
            conversation_history.pop()
            return f"API Error: {data}"

    except requests.exceptions.HTTPError as e:
        conversation_history.pop()
        try:
            details = e.response.json()
        except Exception:
            details = e.response.text if e.response else str(e)
        return f"HTTP Error: {details}"
    except requests.exceptions.RequestException as e:
        conversation_history.pop()
        return f"Request Error: {e}"
    except Exception as e:
        conversation_history.pop()
        return f"Error: {e}"


def reset_conversation():
    """Clear the conversation history."""
    conversation_history.clear()


def chat():
    """Original CLI chatbot interface."""
    if not API_KEY:
        print("GROQ_API_KEY is not set.")
        return

    print("Chatbot started (type 'exit' to quit)\n")
    reset_conversation()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Bye")
            break

        if not user_input:
            print("Bot: Please enter a message.")
            continue

        if user_input.lower() == "exit":
            print("Bot: Bye")
            break

        reply = get_response(user_input)
        print("Bot:", reply)


if __name__ == "__main__":
    chat()
