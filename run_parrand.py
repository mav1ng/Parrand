import randomize

def run():
    print("🎯 Parrand Draw Started!")

    # Get user inputs
    signups = input("📄 Enter the path to the signup file (CSV or Excel): ").strip()
    try:
        n = int(input("🔢 How many participants do you want to draw? ").strip())
    except ValueError:
        print("❌ Invalid number entered.")
        return

    try:
        # Run the random draw
        selected_hashes = randomize.randomize(signups=signups, n=n)
    except Exception as e:
        print(f"❌ An error occurred during randomization: {e}")
        return

    # Output results
    print("\n✅ Selected hashes:")
    for h in selected_hashes:
        print(f"🔹 {h}")

    print("\n🎉 Draw complete!")
