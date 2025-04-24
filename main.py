import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
import os
import re
import randomize
import dataloader
from datetime import datetime

DOWNLOAD_PASSWORD = "azinspire2024"

EMAIL_REGEX = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"

class Parrand:
    def __init__(self, root):
        self.root = root
        root.title("Parrand Draw")
        root.geometry("720x700")
        root.configure(bg="#f7f9fc")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f7f9fc", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), background="#f7f9fc", foreground="#1a1a1a")
        style.configure("TButton", font=("Helvetica", 10), padding=6)

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="Email Signups Random Draw", style="Header.TLabel").pack(pady=(20, 10))

        ttk.Label(self.root, text="Paste emails below:").pack(pady=(10, 2))
        self.textbox = tk.Text(self.root, height=7, width=75, font=("Courier", 10), bd=1, relief="solid",
                               bg="#ffffff", fg="#000000")
        self.textbox.pack(pady=(0, 10))

        ttk.Separator(self.root).pack(fill='x', pady=15)

        frame = ttk.Frame(self.root)
        frame.pack(pady=5)
        ttk.Label(frame, text="Number of people to draw:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.n_entry = ttk.Entry(frame, width=10)
        self.n_entry.grid(row=0, column=1, padx=5)

        self.proceed_button = ttk.Button(self.root, text="Run Random Draw", command=self.proceed)
        self.proceed_button.pack(pady=10)

        ttk.Label(self.root, text="Selected Emails", style="Header.TLabel").pack(pady=(25, 5))
        self.output_text = tk.Text(self.root, height=10, width=75, font=("Courier", 10), bd=1, relief="solid",
                                   bg="#ffffff", fg="#000000")
        self.output_text.pack(pady=10)

        ttk.Separator(self.root).pack(fill='x', pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        self.download_button = ttk.Button(button_frame, text="Download Data Files", command=self.prompt_password)
        self.download_button.grid(row=0, column=0, padx=10)
        self.finish_button = ttk.Button(button_frame, text="Finish", command=self.root.quit)
        self.finish_button.grid(row=0, column=1, padx=10)

    def proceed(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number to draw.")
            return

        pasted_emails = self.textbox.get("1.0", tk.END).strip().splitlines()
        pasted_emails = [e.strip() for e in pasted_emails if e.strip()]
        if not pasted_emails:
            messagebox.showerror("No Emails", "Please paste some emails to proceed.")
            return

        valid_emails = [e for e in pasted_emails if re.fullmatch(EMAIL_REGEX, e)]
        if not valid_emails:
            messagebox.showerror("Invalid Emails", "No valid email addresses found.")
            return

        input_df = pd.DataFrame({"email": valid_emails})

        event_title = simpledialog.askstring("Event Title", "Enter the event name for this draw:")
        if not event_title:
            messagebox.showerror("Missing Title", "Event title is required to proceed.")
            return

        try:
            input_df["email"] = input_df["email"].str.strip().str.lower()

            selected_df = randomize.randomize(signups=input_df, n=n)

            base_df = dataloader.load_base()
            rand_df = dataloader.load_rand(base_df=base_df)

            selected_df = selected_df.merge(rand_df[['hash', 'priority']], on='hash', how='left')

            emails = selected_df['email'].dropna().astype(str).tolist()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(emails))
            self.output_text.update_idletasks()
            self.textbox.delete("1.0", tk.END)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_lines = [f"--- {event_title} | {timestamp} ---"]

            max_email_len = selected_df['email'].apply(len).max()
            max_priority_len = selected_df['priority'].apply(lambda x: len(str(x))).max()

            for _, row in selected_df.iterrows():
                log_lines.append(
                    f"{row['email']: <{max_email_len}} | priority: {str(row['priority']): <{max_priority_len}}")

            log_lines.append("\n")
            log_path = dataloader.get_data_path("log.txt")
            with open(log_path, "a") as log_file:
                log_file.write("\n".join(log_lines))

        except Exception as e:
            messagebox.showerror("Randomization failed", str(e))

    def prompt_password(self):
        password = simpledialog.askstring("Password Required", "Enter password to download files:", show='*')
        if password and password == DOWNLOAD_PASSWORD:
            self.download_files()
        else:
            messagebox.showerror("Access Denied", "Incorrect password. Cannot download files.")

    def download_files(self):
        rand_file = "data/rand.csv"
        base_file = "data/base.csv"

        if not os.path.exists(rand_file) or not os.path.exists(base_file):
            messagebox.showerror("Error", "Required data files do not exist.")
            return

        save_rand_path = tk.filedialog.asksaveasfilename(title="Save rand.csv", defaultextension=".csv",
                                                         filetypes=[("CSV Files", "*.csv")])
        if save_rand_path:
            try:
                with open(rand_file, 'r') as src, open(save_rand_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not save rand.csv: {e}")

        save_base_path = tk.filedialog.asksaveasfilename(title="Save base.csv", defaultextension=".csv",
                                                         filetypes=[("CSV Files", "*.csv")])
        if save_base_path:
            try:
                with open(base_file, 'r') as src, open(save_base_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not save base.csv: {e}")
            else:
                messagebox.showinfo("Download Complete", "Files downloaded successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Parrand(root)
    root.mainloop()
