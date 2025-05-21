import subprocess
import tempfile
import os
import base64
from groq import Groq

def encode_image_from_clipboard():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    result = subprocess.run(["pngpaste", tmp_path], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("No image found in clipboard or pngpaste not installed.")
    with open(tmp_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    os.remove(tmp_path)
    return encoded

base64_image = encode_image_from_clipboard()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Extract only the LaTeX code needed to render the following image. "
                        "Do not include any explanations, comments, or formatting such as ```latex or ```; Do not include any LaTeX preamble or document class, or any packages, or any begin document or any other unnecessary headers or text. "
                        "output only the raw LaTeX code."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
)

latex_code = chat_completion.choices[0].message.content
subprocess.run("pbcopy", text=True, input=latex_code)