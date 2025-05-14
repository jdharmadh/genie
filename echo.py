import argparse
import os
from groq import Groq

def main():
    parser = argparse.ArgumentParser(description="Echo a string back to the console.")
    parser.add_argument("message", help="The string to echo back.")
    args = parser.parse_args()

    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    main()
