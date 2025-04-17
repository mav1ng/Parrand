import dataloader

def randomize(signups, n):
    base_df = dataloader.load_base()
    base_df = dataloader.update_base(input_file=signups)

    # Load or update rand_df (includes all hashes, historical and new)
    rand_df = dataloader.load_rand(base_df=base_df)

    # Get only the hashes related to current signups
    signup_hashes = base_df['hash'].tolist()
    signup_rand_df = rand_df[rand_df['hash'].isin(signup_hashes)].copy()

    # Sample n hashes weighted by priority (from signups only)
    weights = signup_rand_df['priority'].astype(float)
    selected_df = signup_rand_df.sample(n=n, weights=weights, replace=False, random_state=None)

    # Update priorities only for hashes involved in this round
    rand_df.loc[rand_df['hash'].isin(selected_df['hash']), 'priority'] = 1
    rand_df.loc[rand_df['hash'].isin(signup_hashes) & ~rand_df['hash'].isin(selected_df['hash']), 'priority'] += 1

    # Save updated rand_df
    dataloader.save_rand(rand_df=rand_df)

    selected_df = selected_df.merge(base_df[['email', 'hash']], on='hash', how='left')

    return selected_df[['email', 'hash']]
