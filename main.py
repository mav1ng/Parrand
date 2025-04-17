import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import randomize
import tempfile
import os


class ParrandGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎉 Parrand Draw")
        master.geometry("650x700")

        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # --- Upload/Input ---
        ttk.Label(self.frame, text="Choose one of the methods to provide signups:").pack(pady=(0, 10))

        self.upload_button = ttk.Button(self.frame, text="📁 Upload Excel or CSV File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        ttk.Label(self.frame, text="OR").pack(pady=5)

        self.textbox = tk.Text(self.frame, height=10, width=70, font=("Courier", 10))
        self.textbox.insert(tk.END, "Paste emails here, one per line...")
        self.textbox.pack(pady=10)

        ttk.Label(self.frame, text="🔢 Number of participants to draw:").pack(pady=(10, 5))
        self.num_entry = ttk.Entry(self.frame, width=10)
        self.num_entry.pack()

        self.proceed_button = ttk.Button(self.frame, text="✅ Proceed to Randomize", command=self.proceed)
        self.proceed_button.pack(pady=20)

        # --- Output field (hidden at first) ---
        self.output_label = ttk.Label(self.frame, text="🎯 Selected Participants (hashes):")
        self.output_text = tk.Text(self.frame, height=10, width=70, font=("Courier", 10), wrap="none")
        self.finish_button = ttk.Button(self.frame, text="🏁 Finish", command=self.master.quit)

        self.signups_file = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Signup File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        if file_path:
            self.signups_file = file_path
            messagebox.showinfo("File Selected", f"Selected file:\n{file_path}")

    def proceed(self):
        # Validate number
        try:
            n = int(self.num_entry.get().strip())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Number", "Please enter a valid number of participants to draw.")
            return

        # Get signups source
        if self.signups_file:
            input_file = self.signups_file
        else:
            pasted_text = self.textbox.get("1.0", tk.END).strip()
            emails = [line.strip().lower() for line in pasted_text.splitlines() if "@" in line]
            if not emails:
                messagebox.showerror("Invalid Input", "No valid emails found in pasted content.")
                return
            temp_df = pd.DataFrame({'email': emails})
            tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='', encoding='utf-8')
            temp_df.to_csv(tmpfile.name, index=False)
            input_file = tmpfile.name

        # Preview and confirm
        try:
            preview_df = pd.read_excel(input_file) if input_file.endswith('.xlsx') else pd.read_csv(input_file)
            if 'email' not in preview_df.columns:
                raise ValueError("Input must contain an 'email' column.")
            email_preview = "\n".join(preview_df['email'].astype(str).head(5).tolist())
            confirm = messagebox.askyesno("Confirm", f"{len(preview_df)} signups detected.\n\nPreview:\n{email_preview}\n\nContinue?")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load input file:\n{e}")
            return

        if not confirm:
            return

        # Run draw
        try:
            selected_df = randomize.randomize(signups=input_file, n=n)
            emails = selected_df['email'].dropna().astype(str).tolist()

            # Show in GUI text output
            self.output_label.pack(pady=(10, 5))
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\n".join(emails))
            self.output_text.pack(pady=(0, 20))
            self.finish_button.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Randomization failed:\n{e}")
        finally:
            if not self.signups_file and os.path.exists(input_file):
                os.remove(input_file)


def run():
    root = tk.Tk()
    app = ParrandGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()
