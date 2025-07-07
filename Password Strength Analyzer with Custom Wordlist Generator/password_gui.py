import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn
import nltk
import string

# Download NLTK words corpus if not present
nltk.download('words')
from nltk.corpus import words

def analyze_password_gui():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    result = zxcvbn(password)
    msg = (f"Strength Score: {result['score']}/4\n"
           f"Guesses: {result['guesses']}\n"
           f"Feedback: {result['feedback']['warning'] or 'No warnings.'}")
    messagebox.showinfo("Password Analysis", msg)

def generate_wordlist_gui():
    inputs = entry_inputs.get()
    if not inputs:
        messagebox.showerror("Error", "Enter at least one input (name, pet, date).")
        return

    leet_subs = str.maketrans('aeios', '43105')
    input_list = inputs.split()
    years = range(1990, 2031)
    wordlist = set()

    for word in input_list:
        wordlist.add(word.lower())
        wordlist.add(word.upper())
        wordlist.add(word.capitalize())
        wordlist.add(word.translate(leet_subs))
        for year in years:
            wordlist.add(f"{word}{year}")
            wordlist.add(f"{word.translate(leet_subs)}{year}")

    # Add common words
    common_words = [w for w in words.words() if len(w) <= 5]
    wordlist.update(common_words)

    with open("custom_wordlist_gui.txt", 'w') as f:
        for word in sorted(wordlist):
            f.write(f"{word}\n")

    messagebox.showinfo("Success", "Wordlist exported to 'custom_wordlist_gui.txt'")

# GUI Setup
root = tk.Tk()
root.title("Password Strength Analyzer")

tk.Label(root, text="Enter Password:").pack()
entry_password = tk.Entry(root, show='*', width=30)
entry_password.pack()

tk.Button(root, text="Analyze Password", command=analyze_password_gui).pack(pady=5)

tk.Label(root, text="Enter Inputs (name, date, pet) separated by space:").pack()
entry_inputs = tk.Entry(root, width=50)
entry_inputs.pack()

tk.Button(root, text="Generate Wordlist", command=generate_wordlist_gui).pack(pady=5)

root.mainloop()
