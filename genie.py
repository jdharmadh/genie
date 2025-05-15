import argparse
import os
from groq import Groq
import sys
import termios
import tty

def main():
    parser = argparse.ArgumentParser(description="Pass in a string.")
    parser.add_argument("message", help="The string passed in.")
    args = parser.parse_args()

    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": (
                "You are a CLI command generator for macOS.\n"
                "Your job is to output a single shell command that directly satisfies the user's request.\n"
                "Respond with only the exact command, with no explanation, no punctuation, no markdown formatting, and no extra text.\n"
                "Do not include quotation marks, code blocks, or any other wrapper.\n"
                "Do not prefix your response with 'Command:', 'Here is:', or anything similar.\n"
                "The command should be compatible with macOS (zsh environment).\n"
                "If there are multiple valid ways to do it, pick the most concise and standard one.\n\n"
                "If the user mentions 'attu' or 'my attu', this refers to an SSH box with the hostname jayd1903@attu.cs.washington.edu. You should include that in the command if required. If the command is related to files on attu, prefix the filepath with /homes/iws/jayd1903.\n"
                "Examples:\n"
                "Input: list all files including hidden ones\n"
                "Output: ls -a\n\n"
                "Input: find all .txt files in the current directory\n"
                "Output: find . -name '*.txt'\n\n"
                "Input: show the current Wi-Fi network\n"
                "Output: networksetup -getairportnetwork en0\n\n"
                "Input: create a zip archive called backup.zip from the folder Documents\n"
                "Output: zip -r backup.zip Documents\n\n"
                "Input: get the current date\n"
                "Output: date\n\n"
                "Input: scp everything in 444 on attu into the current directory\n"
                "Output: scp jayd1903@attu.cs.washington.edu:/homes/iws/444/* .\n\n"
                "Remember: respond with only the shell command for macOS. No extra text."
            ),
        },
        {
            "role": "user",
            "content": args.message,
        }
    ],
    model="llama-3.3-70b-versatile",
)


    print(f"\033[1;36m{chat_completion.choices[0].message.content}\033[0m")
    print("Press Enter to execute the command, or any other key to cancel: ", end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print()  # Move to next line after key press

    if ch == "\r" or ch == "\n":
        os.system(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    main()
