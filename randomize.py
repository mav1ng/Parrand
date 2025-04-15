import dataloader

def randomize(n):
    rand_df = dataloader.load_rand()

    weights = rand_df['priority'].astype(float)

    # Draw 'n' samples with replacement=False (no duplicates) based on priority
    selected_df = rand_df.sample(n=n, weights=weights, replace=False, random_state=None)

    # Update priorities
    rand_df.loc[rand_df['hash'].isin(selected_df['hash']), 'priority'] = 1
    rand_df.loc[~rand_df['hash'].isin(selected_df['hash']), 'priority'] += 1

    # Return selected hashes as list
    return selected_df['hash'].tolist()
