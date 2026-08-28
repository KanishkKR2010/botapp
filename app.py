import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify

APP_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(APP_DIR / "templates"),
            static_folder=str(APP_DIR / "static"))

HISTORY_FILE = APP_DIR / "chat_history.json"

def load_history():
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history[-100:], ensure_ascii=False, indent=2), encoding="utf-8")

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/history")
def history():
    return jsonify(load_history())

@app.post("/api/chat")
def chat():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    # This starter is deliberately offline. Replace generate_local_reply()
    # with a local model runtime in local_model.py.
    reply = generate_local_reply(message)

    h = load_history()
    h.append({"role": "user", "content": message})
    h.append({"role": "assistant", "content": reply})
    save_history(h)
    return jsonify({"reply": reply})

@app.post("/api/run")
def run_code():
    data = request.get_json(force=True)
    code = data.get("code") or ""
    if not code.strip():
        return jsonify({"output": "", "error": "No Python code supplied."}), 400

    # Basic safety restrictions for this educational offline runner.
    blocked = [
        "import os", "from os", "import subprocess", "from subprocess",
        "import socket", "from socket", "import requests", "import urllib",
        "import shutil", "from shutil", "eval(", "exec(", "__import__",
        "open(", "input("
    ]
    lowered = code.lower()
    hit = next((x for x in blocked if x in lowered), None)
    if hit:
        return jsonify({"output": "", "error": f"Blocked for safety: {hit}"}), 400

    with tempfile.TemporaryDirectory() as td:
        script = Path(td) / "program.py"
        script.write_text(code, encoding="utf-8")
        try:
            p = subprocess.run(
                [sys.executable, "-I", str(script)],
                capture_output=True, text=True, timeout=5,
                cwd=td
            )
            return jsonify({
                "output": p.stdout,
                "error": p.stderr,
                "returncode": p.returncode
            })
        except subprocess.TimeoutExpired:
            return jsonify({"output": "", "error": "Program stopped: 5-second limit reached."}), 408
        except Exception as e:
            return jsonify({"output": "", "error": str(e)}), 500

def generate_local_reply(message):
    m = message.lower()

    if "hello" in m or "hi" in m:
        return "Hello. I am Python AI, an offline Python tutor. Ask me about Python, code, errors, or concepts."

    if "list comprehension" in m:
        return """A list comprehension creates a list in a compact way.

Example:
numbers = [1, 2, 3, 4]
squares = [x * x for x in numbers]

The result is:
[1, 4, 9, 16]

General form:
[expression for item in iterable if condition]"""

    if "for loop" in m:
        return """A for loop repeats code for each item in an iterable.

Example:
for i in range(5):
    print(i)

Output:
0
1
2
3
4"""

    if "if" in m and "else" in m:
        return """An if/else statement chooses between two blocks.

Example:
age = 18

if age >= 18:
    print("Adult")
else:
    print("Not adult")"""

    if "function" in m or "def " in m:
        return """A function is reusable code defined with def.

Example:
def add(a, b):
    return a + b

result = add(2, 3)
print(result)"""

    if "dictionary" in m:
        return """A dictionary stores key-value pairs.

Example:
student = {"name": "Alex", "mark": 95}
print(student["name"])

Dictionaries are mutable and keys should be hashable."""

    if "tuple" in m:
        return """A tuple is an ordered, immutable collection.

Example:
point = (10, 20)
print(point[0])

Unlike a list, a tuple cannot normally be changed after creation."""

    return """I am running in offline mode.

This starter build has a built-in Python tutor for common topics. To make it a full generative chatbot, place a compatible local LLM in the model/ folder and connect it through local_model.py.

You can already use the Code Editor tab to run simple Python programs locally."""

if __name__ == "__main__":
    import webbrowser, threading
    url = "http://127.0.0.1:8765"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=8765, debug=False)
