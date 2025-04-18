import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
import os
import tempfile
import randomize
import dataloader

DOWNLOAD_PASSWORD = "azinspire2024"


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

        # Upload section
        self.upload_button = ttk.Button(self.root, text="Upload Signup File", command=self.upload_file)
        self.upload_button.pack()

        ttk.Label(self.root, text="or paste emails below:").pack(pady=(10, 2))

        self.textbox = tk.Text(self.root, height=7, width=75, font=("Courier", 10), bd=1, relief="solid")
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

        self.output_text = tk.Text(self.root, height=10, width=75, font=("Courier", 10), bd=1, relief="solid", bg="#ffffff")
        self.output_text.pack(pady=10)

        ttk.Separator(self.root).pack(fill='x', pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.download_button = ttk.Button(button_frame, text="Download Data Files", command=self.prompt_password)
        self.download_button.grid(row=0, column=0, padx=10)

        self.finish_button = ttk.Button(button_frame, text="Finish", command=self.root.quit)
        self.finish_button.grid(row=0, column=1, padx=10)

        # Variable to track whether the input file was set
        self.selected_file = None

    def upload_file(self):
        self.selected_file = filedialog.askopenfilename(
            title="Select Signups File",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if self.selected_file:
            messagebox.showinfo("File Selected", f"Selected file:\n{self.selected_file}")

    def proceed(self):
        try:
            # Validate the number of people to draw
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number to draw.")
            return

        # If no file is selected, use the pasted emails
        if not hasattr(self, 'selected_file') or self.selected_file is None:
            pasted_emails = self.textbox.get("1.0", tk.END).strip().splitlines()
            pasted_emails = [e.strip() for e in pasted_emails if e.strip()]
            if not pasted_emails:
                messagebox.showerror("No Emails", "Please paste some emails or upload a file.")
                return

            # Create a DataFrame from pasted emails
            input_df = pd.DataFrame({"email": pasted_emails})
        else:
            # If a file is selected, read the file into a DataFrame
            if self.selected_file.endswith('.xlsx'):
                input_df = pd.read_excel(self.selected_file)
            else:
                input_df = pd.read_csv(self.selected_file)

        # Call the randomizer with the DataFrame of emails, and the number of people to select
        try:
            # Pass the DataFrame directly, not the file path
            selected_df = randomize.randomize(signups=input_df, n=n)

            # Get the selected emails and display them in the output text area
            emails = selected_df['email'].dropna().astype(str).tolist()

            # Clear the previous output and insert the selected emails
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(emails))

            # After randomizing, clear the text box if you want to allow new data input
            self.textbox.delete("1.0", tk.END)

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

        save_rand_path = filedialog.asksaveasfilename(title="Save rand.csv", defaultextension=".csv",
                                                      filetypes=[("CSV Files", "*.csv")])
        if save_rand_path:
            try:
                with open(rand_file, 'r') as src, open(save_rand_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not save rand.csv: {e}")
                return

        save_base_path = filedialog.asksaveasfilename(title="Save base.csv", defaultextension=".csv",
                                                      filetypes=[("CSV Files", "*.csv")])
        if save_base_path:
            try:
                with open(base_file, 'r') as src, open(save_base_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not save base.csv: {e}")
                return

        messagebox.showinfo("Download Complete", "Files downloaded successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Parrand(root)
    root.mainloop()
