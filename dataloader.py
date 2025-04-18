import pandas as pd
import hashlib
import os


def load_rand(base_df, rand_file="data/rand.csv"):
    try:
        # Load existing rand file
        rand_df = pd.read_csv(rand_file)

        # Find hashes in base_df not already in rand_df
        new_hashes_df = base_df[['hash']][~base_df['hash'].isin(rand_df['hash'])].copy()
        new_hashes_df['priority'] = 1

        # Append new hashes to rand_df
        rand_df = pd.concat([rand_df, new_hashes_df], ignore_index=True)

    except FileNotFoundError:
        # If the file doesn't exist, create it from base_df
        rand_df = base_df[['hash']].copy()
        rand_df['priority'] = 1
    return rand_df


def save_rand(rand_df, rand_file="data/rand.csv"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(rand_file), exist_ok=True)
    # Save to CSV
    rand_df.to_csv(rand_file, index=False)

# Function to hash the email
def hash_email(email: str) -> str:
    normalized = email.strip().lower().encode('utf-8')
    return hashlib.sha256(normalized).hexdigest()

# Load the base dataframe
def load_base(base_file="data/base.csv", email_column="email"):
    try:
        base_df = pd.read_csv(base_file)
    except FileNotFoundError:
        base_df = pd.DataFrame(columns=[email_column, 'hash'])
    return base_df

# Save the base dataframe
def save_base(base_df, base_file="data/base.csv"):
    os.makedirs(os.path.dirname(base_file), exist_ok=True)
    base_df.to_csv(base_file, index=False)


def update_base(input_df, output_base_file="data/base.csv", base_file="data/base.csv", email_column="email", return_signups_only=False):
    base_df = load_base(base_file=base_file, email_column=email_column)

    # Normalize input emails
    input_df[email_column] = input_df[email_column].str.strip().str.lower()

    # Find new emails not in base
    new_emails_df = input_df[~input_df[email_column].isin(base_df[email_column])].copy()

    # Hash new emails
    new_emails_df['hash'] = new_emails_df[email_column].apply(hash_email)

    # Combine and deduplicate
    combined_df = pd.concat([base_df, new_emails_df], ignore_index=True).drop_duplicates(subset=[email_column])

    # Save updated base
    save_base(combined_df, base_file=output_base_file)

    base_df = load_base(base_file=base_file, email_column=email_column)
    input_df = input_df.merge(base_df[['email', 'hash']], on='email', how='left')
    print(input_df)

    if return_signups_only:
        return combined_df, input_df
    else:
        return combined_df


