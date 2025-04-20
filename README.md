# Parrand

**Parrand** is a simple desktop app to randomly select participants from a list of email signups. It supports weighted draws based on past selections and ensures fairness across multiple rounds.

Built with **Python** and **Tkinter**, it allows input via pasted emails or uploaded CSV/XLSX files, and stores history for reproducible and consistent results over time.

---

## Features

- Paste emails directly or upload a signup file (CSV or Excel)
- Weighted random selection using priority values
- Download result files with password protection
- Saves and updates data across sessions (`base.csv`, `rand.csv`)
- Avoids reselecting winners too frequently by increasing weights

---

## Requirements

- Python 3.8+
- pandas

Install dependencies:

```bash
pip install pandas
```

---

## Usage

1. Run the app:

```bash
python main.py
```

2. Paste email addresses into the textbox _or_ upload a file.
3. Enter the number of people to draw.
4. Click **Run Random Draw**.
5. View the selected emails and optionally download updated data files (`rand.csv`, `base.csv`).

---

## Download Protection

To download internal tracking files (`rand.csv`, `base.csv`), enter the password that you have set:


---

## Data Files

- `base.csv` – All known signups with hashed emails.
- `rand.csv` – Internal file tracking selection weights and history.

These files update automatically after each draw.

---

## Logic Overview

- Emails are normalized (trimmed, lowercased) and hashed (SHA256).
- New signups are added to `base.csv`, and given default weight.
- Participants are randomly drawn with weights.
  - Winners: weight reset to 1
  - Non-winners: weight increases by 1 (increasing future chance)
- Reproducible thanks to persistent CSV storage.

---

## Project Structure

```
.
├── app.py           # GUI application (Tkinter)
├── randomize.py     # Core logic for random draw
├── dataloader.py    # Handles loading/saving data files
├── data/
│   ├── base.csv     # Stores all known emails and hashes
│   └── rand.csv     # Tracks priority values per email hash
```

---

## License

MIT License. Use it, modify it, share it – just give credit. 💙
