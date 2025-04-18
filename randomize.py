import dataloader
import pandas as pd
import hashlib

def randomize(signups, n):
    # Check if 'signups' is a DataFrame or a string and handle accordingly
    if isinstance(signups, str):
        signup_df = parse_signup_emails(signups)  # If it's a string, parse it as emails
    elif isinstance(signups, pd.DataFrame):
        signup_df = signups  # If it's a DataFrame, use it directly
    else:
        raise ValueError("Invalid signups format. Expected string or DataFrame.")

    if signup_df.empty:
        raise ValueError("No valid signups provided.")

    # Update base with signups and get both: updated base + new signups only
    base_df, signup_df = dataloader.update_base(input_df=signup_df, return_signups_only=True)

    # Ensure base_df contains the required columns
    if 'email' not in base_df.columns or 'hash' not in base_df.columns:
        raise ValueError("Base DataFrame is missing required columns: 'email' or 'hash'.")

    # Load or update rand_df based only on the new signups
    rand_df = dataloader.load_rand(base_df=signup_df)

    # Ensure rand_df contains the required column for hashing
    if 'hash' not in rand_df.columns or 'priority' not in rand_df.columns:
        raise ValueError("Rand DataFrame is missing required columns: 'hash' or 'priority'.")

    # Get only the hashes from the new signups
    signup_hashes = signup_df['hash'].tolist()
    signup_rand_df = rand_df[rand_df['hash'].isin(signup_hashes)].copy()

    # Ensure priority values are valid (non-zero and numeric)
    signup_rand_df['priority'] = pd.to_numeric(signup_rand_df['priority'], errors='coerce').fillna(1).clip(lower=1)

    # Check if there are valid entries to sample from
    if signup_rand_df.empty:
        raise ValueError("No valid signups found to randomize.")

    # Ensure valid weights (sum should not be zero)
    if signup_rand_df['priority'].sum() == 0:
        raise ValueError("Invalid weights: weights sum to zero.")

    # Sample n hashes weighted by priority (from signups only)
    weights = signup_rand_df['priority'].astype(float)
    selected_df = signup_rand_df.sample(n=n, weights=weights, replace=False, random_state=None)

    # Update priorities only for hashes involved in this round
    rand_df.loc[rand_df['hash'].isin(selected_df['hash']), 'priority'] = 1
    rand_df.loc[rand_df['hash'].isin(signup_hashes) & ~rand_df['hash'].isin(selected_df['hash']), 'priority'] += 1

    # Save updated rand_df
    dataloader.save_rand(rand_df=rand_df)

    # Merge selected hashes back to get emails
    selected_df = selected_df.merge(base_df[['email', 'hash']], on='hash', how='left')

    # Return selected emails and hashes
    return selected_df[['email', 'hash']]


def parse_signup_emails(email_text):
    # Clean up and split the emails (only if email_text is a string)
    if isinstance(email_text, str):
        emails = email_text.splitlines()
        emails = [email.strip() for email in emails if email.strip() != ""]  # Remove empty lines or spaces

        # If no valid emails, raise an error
        if not emails:
            raise ValueError("No valid email addresses found in the input.")

        # Create a DataFrame with the emails
        signup_df = pd.DataFrame(emails, columns=['email'])

        # Generate corresponding hashes for the emails
        signup_df['hash'] = signup_df['email'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
        return signup_df

    raise ValueError("Expected input as a string for emails, but got something else.")
