import dataloader
import pandas as pd
import hashlib

def randomize(signups, n):
    import dataloader

    if isinstance(signups, str):
        signup_df = parse_signup_emails(signups)
    elif isinstance(signups, pd.DataFrame):
        signup_df = signups
    else:
        raise ValueError("Invalid signups format. Expected string or DataFrame.")

    if signup_df.empty:
        raise ValueError("No valid signups provided.")

    base_df, signup_df = dataloader.update_base(input_df=signup_df, return_signups_only=True)

    if 'email' not in base_df.columns or 'hash' not in base_df.columns:
        raise ValueError("Base DataFrame is missing required columns: 'email' or 'hash'.")

    rand_df = dataloader.load_rand(base_df=signup_df)

    if 'hash' not in rand_df.columns or 'priority' not in rand_df.columns:
        raise ValueError("Rand DataFrame is missing required columns: 'hash' or 'priority'.")

    signup_hashes = signup_df['hash'].tolist()
    signup_rand_df = rand_df[rand_df['hash'].isin(signup_hashes)].copy()

    signup_rand_df['priority'] = pd.to_numeric(signup_rand_df['priority'], errors='coerce').fillna(1).clip(lower=1)

    if signup_rand_df.empty:
        raise ValueError("No valid signups found to randomize.")

    if signup_rand_df['priority'].sum() == 0:
        raise ValueError("Invalid weights: weights sum to zero.")

    # Save the original priorities used for weighting before modifying
    priority_map = signup_rand_df.set_index('hash')['priority'].to_dict()

    weights = signup_rand_df['priority'].astype(float)
    selected_df = signup_rand_df.sample(n=n, weights=weights, replace=False, random_state=None)

    rand_df.loc[rand_df['hash'].isin(selected_df['hash']), 'priority'] = 1
    rand_df.loc[rand_df['hash'].isin(signup_hashes) & ~rand_df['hash'].isin(selected_df['hash']), 'priority'] += 1

    dataloader.save_rand(rand_df=rand_df)

    selected_df = selected_df.merge(base_df[['email', 'hash']], on='hash', how='left')

    # Add the original priority values before updating
    selected_df['used_priority'] = selected_df['hash'].map(priority_map)

    return selected_df[['email', 'hash', 'used_priority']]



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
