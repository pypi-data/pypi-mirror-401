import os
import subprocess

try:
    from groq import Groq
except ImportError:
    subprocess.check_call(["pip", "install", "groq"])
    from groq import Groq


# HARD-CODED KEY (for 1-day private use)
API_KEY = "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"


def askOmi(prompt: str) -> str:
    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content


def gen(error: str):
    reply = askOmi(error)

    with open("code.py", "w", encoding="utf-8") as f:
        f.write(reply)

    print("Done")


def destroy():
    packages = ["groq", "askOmi"]

    for p in packages:
        try:
            subprocess.check_call(["pip", "uninstall", "-y", p])
        except subprocess.CalledProcessError:
            pass

    if os.path.exists("code.py"):
        os.remove("code.py")
        print("deleted")
