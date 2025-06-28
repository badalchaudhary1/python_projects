import tkinter as tk
from tkinter import messagebox
from icrawler.builtin import GoogleImageCrawler
import threading

def run_downloader():
    kw = kw_box.get().strip()
    num = num_box.get().strip()
    folder = folder_box.get().strip()

    if not kw or not num.isdigit():
        messagebox.showerror("Input error", "Enter valid keyword and number")
        return

    status_lbl.config(text="Starting download...")

    def work():
        try:
            crawler = GoogleImageCrawler(storage={'root_dir': folder or 'images'})
            crawler.crawl(keyword=kw, max_num=int(num))
            status_lbl.config(text=f"Done! Saved in '{folder or 'images'}'")
        except Exception as err:
            print("Error:", err)
            status_lbl.config(text="Something went wrong.")

    threading.Thread(target=work).start()

# GUI setup
root = tk.Tk()
root.title("Img Grabber")
root.geometry("400x300")
root.configure(bg="#dff")

tk.Label(root, text="Google Image Downloader", font=("Arial", 14, "bold"), bg="#dff").pack(pady=10)

tk.Label(root, text="Keyword:", bg="#dff").pack()
kw_box = tk.Entry(root, width=30)
kw_box.pack(pady=4)

tk.Label(root, text="How many images:", bg="#dff").pack()
num_box = tk.Entry(root, width=30)
num_box.insert(0, "5")
num_box.pack(pady=4)

tk.Label(root, text="Folder name:", bg="#dff").pack()
folder_box = tk.Entry(root, width=30)
folder_box.insert(0, "images")
folder_box.pack(pady=4)

tk.Button(root, text="Download", command=run_downloader, bg="green", fg="white").pack(pady=10)

status_lbl = tk.Label(root, text="", bg="#dff", fg="darkblue")
status_lbl.pack()

root.mainloop()
