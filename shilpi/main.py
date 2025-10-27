import json
import random
import asyncio
import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator


# ---------------------- Load Quotes ----------------------
def load_quotes(filename="quotes.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "❌ quotes.json file not found!")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", "❌ Invalid JSON format in quotes.json.")
        return {}


# ---------------------- Translation ----------------------
async def translate_to_english_async(text):
    translator = Translator()
    translation = await translator.translate(text, dest='en')
    return translation.text


def translate_to_english(text):
    try:
        return asyncio.run(translate_to_english_async(text))
    except Exception as e:
        return f"(⚠️ Translation failed: {e})"


# ---------------------- Show Quote ----------------------
def show_quote():
    language = language_var.get()
    if not language:
        messagebox.showwarning("Warning", "Please select a language!")
        return

    quotes_list = quotes.get(language, [])
    if not quotes_list:
        messagebox.showwarning("Warning", f"No quotes found for {language}.")
        return

    quote = random.choice(quotes_list)
    translation = translate_to_english(quote)

    quote_text.delete(1.0, tk.END)
    translation_text.delete(1.0, tk.END)

    quote_text.insert(tk.END, f"💬 Quote in {language}:\n\n{quote}")
    translation_text.insert(tk.END, f"🌎 English Translation:\n\n{translation}")


# ---------------------- Main GUI ----------------------
quotes = load_quotes()
if not quotes:
    exit()

root = tk.Tk()
root.title("🌐 Multilingual Quote Generator")
root.geometry("600x400")
root.resizable(False, False)

# Label
ttk.Label(root, text="Select Language:", font=("Arial", 12)).pack(pady=10)

# Dropdown
languages = list(quotes.keys())
language_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=language_var, values=languages, state="readonly")
combo.pack(pady=5)
if languages:
    combo.current(0)

# Button
ttk.Button(root, text="Show Random Quote", command=show_quote).pack(pady=10)

# Text Areas
quote_text = tk.Text(root, height=5, wrap="word", font=("Nirmala UI", 11), bg="#f0f8ff")
quote_text.pack(padx=20, pady=5, fill="both", expand=True)

translation_text = tk.Text(root, height=5, wrap="word", font=("Arial", 11), bg="#e6ffe6")
translation_text.pack(padx=20, pady=5, fill="both", expand=True)

root.mainloop()
