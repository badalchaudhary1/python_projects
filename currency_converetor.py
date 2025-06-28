import tkinter as tk
from tkinter import ttk, messagebox
import requests

def do_convert():
    f = from_box.get().strip()
    t = to_box.get().strip()
    amt = amt_box.get().strip()

    if not amt:
        messagebox.showerror("Missing", "Amount is empty.")
        return

    try:
        val = float(amt)
    except:
        messagebox.showerror("Invalid", "Enter a valid number")
        return

    try:
        api = f"https://api.exchangerate.host/convert?from={f}&to={t}&amount={val}"
        r = requests.get(api)
        data = r.json()
        if data.get("result") is not None:
            res = round(data["result"], 4)
            result_lbl.config(text=f"{val} {f} = {res} {t}")
        else:
            result_lbl.config(text="Conversion error.")
    except Exception as err:
        messagebox.showerror("Error", str(err))

# UI setup
win = tk.Tk()
win.title("Currency Tool")
win.geometry("360x280")
win.config(bg='#ffe')

currs = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD"]

tk.Label(win, text="Currency Converter", font=('Arial', 14, 'bold'), bg='#ffe').pack(pady=10)

tk.Label(win, text="From", bg='#ffe').pack()
from_box = ttk.Combobox(win, values=currs, width=15)
from_box.set("USD")
from_box.pack(pady=3)

tk.Label(win, text="To", bg='#ffe').pack()
to_box = ttk.Combobox(win, values=currs, width=15)
to_box.set("INR")
to_box.pack(pady=3)

tk.Label(win, text="Amount", bg='#ffe').pack()
amt_box = tk.Entry(win, width=20)
amt_box.pack(pady=5)

tk.Button(win, text="Convert", command=do_convert, bg='green', fg='white').pack(pady=10)

result_lbl = tk.Label(win, text="", font=('Arial', 12), bg='#ffe')
result_lbl.pack()

win.mainloop()
