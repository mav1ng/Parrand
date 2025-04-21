import pandas as pd
import hashlib
import os
import sys
from pathlib import Path

# Get path to folder where the EXE or script is running
def get_base_path():
    if getattr(sys, 'frozen', False):  # Running as a bundled exe
        return Path(sys.executable).parent
    else:  # Running as a .py script
        return Path(__file__).parent

# Get a path to a file inside the "data" folder
def get_data_path(filename):
    base_path = get_base_path()
    data_dir = base_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir / filename)

def load_rand(rand_file=None, base_df=None):
    if rand_file is None:
        rand_file = get_data_path("rand.csv")

    try:
        rand_df = pd.read_csv(rand_file)
        new_hashes_df = base_df[['hash']][~base_df['hash'].isin(rand_df['hash'])].copy()
        new_hashes_df['priority'] = 1
        rand_df = pd.concat([rand_df, new_hashes_df], ignore_index=True)
    except FileNotFoundError:
        rand_df = base_df[['hash']].copy()
        rand_df['priority'] = 1
    return rand_df

def save_rand(rand_df, rand_file=None):
    if rand_file is None:
        rand_file = get_data_path("rand.csv")
    rand_df.to_csv(rand_file, index=False)

def hash_email(email: str) -> str:
    normalized = email.strip().lower().encode('utf-8')
    return hashlib.sha256(normalized).hexdigest()

def load_base(base_file=None, email_column="email"):
    if base_file is None:
        base_file = get_data_path("base.csv")
    try:
        base_df = pd.read_csv(base_file)
    except FileNotFoundError:
        base_df = pd.DataFrame(columns=[email_column, 'hash'])
    return base_df

def save_base(base_df, base_file=None):
    if base_file is None:
        base_file = get_data_path("base.csv")
    base_df.to_csv(base_file, index=False)

def update_base(input_df, output_base_file=None, base_file=None, email_column="email", return_signups_only=False):
    base_df = load_base(base_file=base_file, email_column=email_column)

    input_df[email_column] = input_df[email_column].str.strip().str.lower()
    new_emails_df = input_df[~input_df[email_column].isin(base_df[email_column])].copy()
    new_emails_df['hash'] = new_emails_df[email_column].apply(hash_email)

    combined_df = pd.concat([base_df, new_emails_df], ignore_index=True).drop_duplicates(subset=[email_column])
    save_base(combined_df, base_file=output_base_file)

    base_df = load_base(base_file=base_file, email_column=email_column)
    input_df = input_df.merge(base_df[['email', 'hash']], on='email', how='left')
    print(input_df)

    if return_signups_only:
        return combined_df, input_df
    else:
        return combined_df
