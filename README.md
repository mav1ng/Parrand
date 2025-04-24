# Parrand - Email Signups Random Draw Tool

Parrand is a Python application designed to facilitate the random selection of participants from email signups. This tool allows users to upload signup lists or paste emails, select the number of participants, and then perform a weighted random draw. It also provides an option to download the resulting data files for further use.

---

## Features

- **Email Paste**: Users can paste emails directly into a text area.
- **Random Draw**: After selecting the number of participants to draw, the application performs a weighted random draw based on pre-defined priorities.
- **Event Logging**: Logs are created with a timestamp and details of the event, including the selected emails and their associated priorities.
- **Downloadable Data Files**: Allows users to download the data files (`rand.csv` and `base.csv`), which contain the list of all participants and their assigned priorities.
- **Password Protection**: A password is required before downloading the data files to ensure security.

---

## Installation

To run the Parrand app, you need to have Python installed on your system along with the required dependencies. Below are the installation steps.

1. Clone or download the repository:

    ```bash
    git clone https://github.com/yourusername/parrand.git
    ```

2. Install the necessary Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. You may need to install `py2app` (for macOS users) or any other packaging tool if you want to convert this into a standalone application. 

---

## Usage

1. **Running the App:**
    - To run the app, execute the following:

    ```bash
    python main.py
    ```

    - The app will open a GUI where you can upload a CSV or Excel file containing email signups or paste emails directly.
    - Once you input the number of participants to draw and provide an event title, the app will display the results in a formatted manner.

2. **Password Protection for File Download:**
    - After running the draw, you can download the resulting data files (`rand.csv` and `base.csv`). A password is required to ensure secure access to these files.
    - The default password is: `azinspire2024`.

3. **Log Files:**
    - The application logs each draw event, including the selected emails and their priorities, to a log file (`log.txt`). The log entries are timestamped and can be reviewed for reference.

---

## Code Overview

### main.py
The main GUI and event logic for the Parrand app. It uses the `tkinter` library to create the user interface. Key functions include:
- **Upload Email File**: Allows users to upload an email signup file in `.csv` or `.xlsx` format.
- **Random Draw**: Performs the random draw based on email data and user input.
- **Logging**: Creates a log of the random draw event, capturing the selected emails and their priorities.
- **Password Protection**: Asks for a password before downloading the data files.

### randomize.py
Contains the core logic for randomizing the email signups and selecting participants. The `randomize()` function takes the signups DataFrame and the number of participants to draw, returning a DataFrame with selected emails and their priorities.

### dataloader.py
Handles the loading, saving, and updating of the `rand.csv` and `base.csv` files. These files store the email hashes and their associated priorities.

### setup.py
A setup script for packaging the app into a standalone application using `py2app` (for macOS). It specifies the necessary dependencies and configuration for packaging.

### run_parrand.py
A simple script for running Parrand from the command line. This script allows users to input file paths and the number of participants to draw directly in the terminal.

---

## Development

### Dependencies

- `tkinter`: For creating the GUI.
- `pandas`: For handling the email signup data.
- `openpyxl` (if working with `.xlsx` files): For reading and writing Excel files.
- `py2app` (optional, for macOS packaging): For packaging the app into a standalone application.

### How to Contribute

1. Fork the repository.
2. Clone your fork to your local machine.
3. Create a new branch for your feature or bug fix.
4. Write your code, tests, and documentation.
5. Push your changes and create a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

