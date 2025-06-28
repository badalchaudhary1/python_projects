import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import requests
import time
import numpy as np
from sklearn.linear_model import LinearRegression

# NSE stock list (can add more)
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "SBIN.NS", "WIPRO.NS", "HCLTECH.NS", "BHARTIARTL.NS"
]

def get_data(symb, sdate, edate):
    try:
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        df = yf.download(symb, start=sdate, end=edate, session=s)
        if df.empty:
            raise Exception("Empty data")
        return df
    except yf.exceptions.YFRateLimitError:
        print("Rate limit hit. Pausing...")
        time.sleep(60)
        return get_data(symb, sdate, edate)
    except Exception as ex:
        print("Fetch error:", ex)
        messagebox.showerror("Error", str(ex))
        return None

def analyse():
    sym = symSel.get().strip()
    try:
        sd = datetime.datetime.strptime(startBox.get(), "%Y-%m-%d")
        ed = datetime.datetime.strptime(endBox.get(), "%Y-%m-%d")
    except:
        messagebox.showwarning("Date Format", "Use YYYY-MM-DD format")
        return

    df = get_data(sym, sd, ed)
    if df is None or df.empty:
        return

    df = df.reset_index()
    df['date_num'] = df['Date'].map(datetime.datetime.toordinal)
    x = np.array(df['date_num']).reshape(-1, 1)
    y = np.array(df['Close']).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, y)
    pred = model.predict(x)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df['Date'], y, label='Close', color='cyan')
    ax.plot(df['Date'], pred, label='Trend', color='orange')
    ax.set_title(f"{sym} Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')

    chart = FigureCanvasTkAgg(fig, master=win)
    chart.draw()
    chart.get_tk_widget().pack(pady=10)

# UI
win = tk.Tk()
win.geometry('850x700')
win.title("NSE Stock Viewer")
win.configure(bg='black')

tk.Label(win, text="Select NSE Stock:", fg='white', bg='black').pack(pady=5)
symSel = ttk.Combobox(win, values=stocks, width=30)
symSel.set("INFY.NS")
symSel.pack()

tk.Label(win, text="Start Date (YYYY-MM-DD):", fg='white', bg='black').pack()
startBox = tk.Entry(win, width=30)
startBox.insert(0, "2024-01-01")
startBox.pack(pady=5)

tk.Label(win, text="End Date (YYYY-MM-DD):", fg='white', bg='black').pack()
endBox = tk.Entry(win, width=30)
endBox.insert(0, "2025-01-01")
endBox.pack(pady=5)

tk.Button(win, text="Analyze", command=analyse, bg='green', fg='white').pack(pady=10)

win.mainloop()
