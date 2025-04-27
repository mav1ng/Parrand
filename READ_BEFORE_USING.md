# AZInspire Events Participant Randomizer

## Introduction

Welcome to the Participant Randomizer. This application is designed to ensure fair and balanced selection of participants for our events. It incorporates a weighted randomization process that increases the chances for applicants who were not selected in previous events.

## Key Features

- Fair randomized selection process
- Increased chances for previously unselected participants
- Support for initial draws and redraws
- Logging of all randomization results

## Important Notes

- **Do NOT move the App or the data folder.** 
- The application must be executed within the Box-Folder to ensure results are synchronized, up-to-date, and visible to all authorized personnel.

## How to Use the Participant Randomizer

### Prerequisites

1. Ensure Box Drive is installed on your work laptop and you can access your Box folders via Finder.
2. Verify that your laptop recognizes the app (Parrand_MacOS) as an executable file.
   - If not, run the following command in your terminal:
     ```
     chmod +x Path/to/Parrand_MacOS
     ```

### Steps for Initial Draw

1. Run Parrand_MacOS by either:
   - Double-clicking in Finder, or
   - Executing `./Parrand_MacOS` in the Terminal (in the directory where Parrand_MacOS is located)
2. Copy-paste the list of sign-up emails from the AZInspire sign-up form into the first text box.
   - **Important:** Exclude organizers who are guaranteed a spot.
3. Choose the number of available seats.
4. Click on the "Run Random Draw" button.
5. Enter the name for the Event in the pop-up box and press OK.
6. Copy the emails of the selected participants from the lower text box.
7. Make note of the selected participants.
8. Click "Finish" to complete the process.

### Redraw Process

In case of participant cancellations:

1. Follow steps 1-2 from the initial draw process.
2. Input only the emails of applicants who have not yet secured a spot.
3. Adjust the "number of people to draw" to match the newly available spots.
4. Name the event using the format: "Original Event Name - Redraw #X" (where X is the redraw number).
5. Complete steps 5-8 from the initial draw process.

## Accessing Draw Results

You can review all randomized draws in the `log.txt` file located in the application folder.
