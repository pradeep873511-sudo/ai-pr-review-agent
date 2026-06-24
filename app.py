import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import threading
from agent import run_agent

def run_review():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a GitHub PR URL.")
        return
    review_output.config(state=tk.NORMAL)
    review_output.delete(1.0, tk.END)
    review_output.insert(tk.END, "Analyzing PR. Please wait...")
    review_output.config(state=tk.DISABLED)
    btn_review.config(state=tk.DISABLED)

    def task():
        try:
            result = run_agent(url)
            review_output.config(state=tk.NORMAL)
            review_output.delete(1.0, tk.END)
            review_output.insert(tk.END, result)
            review_output.config(state=tk.DISABLED)
        except Exception as e:
            review_output.config(state=tk.NORMAL)
            review_output.delete(1.0, tk.END)
            review_output.insert(tk.END, f"Error: {e}")
            review_output.config(state=tk.DISABLED)
        finally:
            btn_review.config(state=tk.NORMAL)

    threading.Thread(target=task).start()

root = tk.Tk()
root.title("AI PR Code Review Agent")
root.geometry("750x600")
root.configure(bg="#0d1117")
root.resizable(False, False)

try:
    icon = Image.open("assets/logo.png")
    icon = icon.resize((32, 32))
    icon_img = ImageTk.PhotoImage(icon)
    root.iconphoto(True, icon_img)
except:
    pass

try:
    logo = Image.open("assets/logo.png")
    logo = logo.resize((70, 70))
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo_img, bg="#0d1117")
    logo_label.pack(pady=(20, 5))
except:
    pass

tk.Label(root, text="AI PR Code Review Agent", font=("Helvetica", 18, "bold"),
         fg="#58a6ff", bg="#0d1117").pack()

tk.Label(root, text="Paste a GitHub Pull Request URL and get an instant AI-powered review.",
         font=("Helvetica", 10), fg="#8b949e", bg="#0d1117").pack(pady=(4, 16))

url_entry = tk.Entry(root, width=70, font=("Helvetica", 11),
                     bg="#161b22", fg="#e6edf3", insertbackground="white",
                     relief="flat", bd=6)
url_entry.pack(pady=(0, 12))

btn_review = tk.Button(root, text="Run Review", command=run_review,
                       bg="#238636", fg="white", font=("Helvetica", 11, "bold"),
                       relief="flat", padx=20, pady=8, cursor="hand2")
btn_review.pack()

tk.Label(root, text="Review Output", font=("Helvetica", 11, "bold"),
         fg="#58a6ff", bg="#0d1117").pack(pady=(16, 4))

review_output = scrolledtext.ScrolledText(root, width=85, height=18,
                                          font=("Helvetica", 10),
                                          bg="#161b22", fg="#e6edf3",
                                          relief="flat", bd=6,
                                          state=tk.DISABLED)
review_output.pack(padx=20)

tk.Label(root, text="Built by Pradeep | Powered by Groq + Llama 3.3",
         font=("Helvetica", 8), fg="#484f58", bg="#0d1117").pack(pady=(10, 0))

root.mainloop()