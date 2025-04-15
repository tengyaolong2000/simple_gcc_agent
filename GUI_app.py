# gui.py
import tkinter as tk
import requests

def send_query():
    user_input = entry.get()
    if not user_input:
        output_text.set("Please enter a query.")
        return

    try:
        res = requests.post("http://localhost:5001/query", json={"query": user_input})
        res.raise_for_status()
        output_text.set(res.json().get("response", "No response from agent."))
    except Exception as e:
        output_text.set(f"Error: {e}")

# GUI setup
root = tk.Tk()
root.title("Agent GUI")

tk.Label(root, text="Enter your command:").pack(pady=5)

entry = tk.Entry(root, width=60)
entry.pack(padx=10)

tk.Button(root, text="Send", command=send_query).pack(pady=5)

output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, wraplength=500, fg="blue").pack(padx=10, pady=10)

root.mainloop()
