import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import os
import tempfile
import randomize
import dataloader

DOWNLOAD_PASSWORD = "azinspire2024"  # Change to your desired password


class EmailDrawApp:
    def __init__(self, root):
        self.root = root
        root.title("Parrand Draw")
        root.geometry("600x600")

        self.label = tk.Label(root, text="Upload an Excel/CSV file with emails or paste emails below:")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.or_label = tk.Label(root, text="OR")
        self.or_label.pack()

        self.textbox = tk.Text(root, height=10, width=70)
        self.textbox.pack(pady=10)

        self.draw_label = tk.Label(root, text="Number of people to draw:")
        self.draw_label.pack()

        self.n_entry = tk.Entry(root)
        self.n_entry.pack()

        self.proceed_button = tk.Button(root, text="Proceed", command=self.proceed)
        self.proceed_button.pack(pady=10)

        self.output_label = tk.Label(root, text="Selected Emails:")
        self.output_label.pack()

        self.output_text = tk.Text(root, height=10, width=70)
        self.output_text.pack(pady=10)

        self.download_button = tk.Button(root, text="Download Data Files", command=self.prompt_password)
        self.download_button.pack(pady=5)

        self.finish_button = tk.Button(root, text="Finish", command=root.quit)
        self.finish_button.pack(pady=10)

        self.selected_file = None

    def upload_file(self):
        self.selected_file = filedialog.askopenfilename(
            title="Select Signups File",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if self.selected_file:
            messagebox.showinfo("File Selected", f"Selected file:\n{self.selected_file}")

    def proceed(self):
        # Get number of people to draw
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number to draw.")
            return

        # Handle pasted emails
        if not self.selected_file:
            pasted_emails = self.textbox.get("1.0", tk.END).strip().splitlines()
            pasted_emails = [e.strip() for e in pasted_emails if e.strip()]
            if not pasted_emails:
                messagebox.showerror("No Emails", "Please paste some emails or upload a file.")
                return

            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")
            df = pd.DataFrame({"email": pasted_emails})
            df.to_csv(temp_file.name, index=False)
            input_file = temp_file.name
        else:
            input_file = self.selected_file

        try:
            selected_df = randomize.randomize(signups=input_file, n=n)
            emails = selected_df['email'].dropna().astype(str).tolist()

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(emails))
        except Exception as e:
            messagebox.showerror("Randomization failed", str(e))

    def prompt_password(self):
        password = simpledialog.askstring("Password Required", "Enter password to download files:", show='*')
        if password == DOWNLOAD_PASSWORD:
            self.download_files()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

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
    app = EmailDrawApp(root)
    root.mainloop()
