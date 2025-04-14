import pandas as pd
import hashlib


def hash_email(email: str) -> str:
    normalized = email.strip().lower().encode('utf-8')
    return hashlib.sha256(normalized).hexdigest()


def load_base(base_file="data/base.csv", email_column="email"):
    try:
        base_df = pd.read_csv(base_file)
    except FileNotFoundError:
        base_df = pd.DataFrame(columns=[email_column, 'hashed_email'])

    # Normalize existing emails
    base_df[email_column] = base_df[email_column].str.strip().str.lower()
    return base_df


def update_base(input_file, output_base_file="data/base.csv", base_file="data/base.csv", email_column="email"):
    base_df = load_base(base_file=base_file, email_column=email_column)
    # --- Load new input ---
    if input_file.endswith('.xlsx'):
        input_df = pd.read_excel(input_file)
    else:
        input_df = pd.read_csv(input_file)

    # Normalize input emails
    input_df[email_column] = input_df[email_column].str.strip().str.lower()
    # Find new emails not in base
    new_emails_df = input_df[~input_df[email_column].isin(base_df[email_column])].copy()

    # Hash new emails
    new_emails_df['hashed_email'] = new_emails_df[email_column].apply(hash_email)

    # Combine and deduplicate
    combined_df = pd.concat([base_df, new_emails_df], ignore_index=True).drop_duplicates(subset=[email_column])

    # Save updated base
    combined_df.to_csv(output_base_file, index=False)
    print(f"Base updated and saved to {output_base_file}")
    return combined_df

