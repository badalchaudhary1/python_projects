import tkinter as tk
from tkinter import messagebox
import random
import datetime
import platform
import os

try:
    import winsound
except ImportError:
    winsound = None


class NumberGuessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🔢 Number Guesser")
        self.master.geometry("420x260")
        self.master.configure(bg="black")  # replaced hex with color name

        self._setup_game()
        self._init_ui()

    def _setup_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

    def _init_ui(self):
        self.title = tk.Label(
            self.master,
            text="🔍 Guess the number (1 - 100)",
            font=("Segoe UI", 13),
            bg="black",  # changed
            fg="white"
        )
        self.title.pack(pady=10)

        self.input_box = tk.Entry(
            self.master,
            font=("Segoe UI", 12),
            justify="center",
            bg="dim gray",  # changed
            fg="white",
            insertbackground="white"
        )
        self.input_box.pack(pady=8)

        self.submit_btn = tk.Button(
            self.master,
            text="Submit",
            font=("Segoe UI", 10),
            bg="dodger blue",  # changed
            fg="white",
            command=self._evaluate_guess
        )
        self.submit_btn.pack()

        self.feedback = tk.Label(
            self.master,
            text="",
            font=("Segoe UI", 11),
            bg="black",  # changed
            fg="white"
        )
        self.feedback.pack(pady=10)

        self.reset_btn = tk.Button(
            self.master,
            text="Reset",
            font=("Segoe UI", 9),
            bg="gray",  # changed
            fg="white",
            command=self._reset_game
        )
        self.reset_btn.pack()

    def _evaluate_guess(self):
        guess = self.input_box.get().strip()

        if not guess.isdigit():
            messagebox.showwarning("Invalid", "Please enter a valid whole number.")
            return

        num = int(guess)
        self.attempts += 1

        if num < self.secret_number:
            self.feedback.config(text="🔽 Too low!")
        elif num > self.secret_number:
            self.feedback.config(text="🔼 Too high!")
        else:
            self._celebrate()
            messagebox.showinfo(" Well Done! ", f"You guess number it in {self.attempts} tries!")
            self._log_score()
            self._reset_game()

    def _reset_game(self):
        self._setup_game()
        self.input_box.delete(0, tk.END)
        self.feedback.config(text="")

    def _celebrate(self):
        system = platform.system()
        if winsound:
            winsound.Beep(1000, 250)
        elif system == "Darwin":
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        elif system == "Linux":
            os.system("play -nq -t alsa synth 0.2 sine 880")

    def _log_score(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{timestamp} | Attempts: {self.attempts}\n"
        with open("guess_scores.log", "a") as file:
            file.write(record)


def main():
    root = tk.Tk()
    NumberGuessGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
