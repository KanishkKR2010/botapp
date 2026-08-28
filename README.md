# Python AI — Offline Desktop App

## What this project is

A Windows desktop-style Python chatbot with:
- Local Flask UI
- Local chat history
- Python code editor
- Local Python execution
- No internet connection required while the application is running

## Important AI note

The included `app.py` contains a small built-in rule-based tutor so the project runs immediately without downloading a model.

For a true generative AI chatbot, add a local LLM runtime/model and replace `generate_local_reply()` with a local inference call. The model must be installed on the computer; cloud APIs are not offline.

## Run from source

1. Install Python 3.11+.
2. Open this folder in Command Prompt.
3. Run:

    python -m pip install -r requirements.txt
    python app.py

4. Your browser opens to the local app.

## Build a Windows EXE

Run:

    build.bat

The result is:

    dist\PythonAI\PythonAI.exe

Copy the entire `dist\PythonAI` folder to another Windows PC.

## Offline behavior

Once Python, the application and any chosen local AI model are installed, the app can run without internet. Do not configure it with OpenAI/ChatGPT cloud APIs if you want it fully offline.

## Security

The code runner has simple keyword restrictions and a short timeout. It is intended for educational code, not as a security sandbox. Do not use it to run untrusted code.
