import os
import pandas as pd
from breezypythongui import EasyFrame
from tkinter import Label, Text, DISABLED
from tkinter import filedialog
from PIL import Image, ImageTk

class DerbyLapTracker(EasyFrame):
       """
    A GUI-based application to track and analyze race results for two aspiring racers competing in a Boy Scout Pinewood derby. This program tracks 10 races for up to 2 racers, and can help troubleshoot the car, and help achieve the fastest times.
    The program allows users to enter racer details, save race times, and analyze race results.
    """
    def __init__(self):
        """Initialize the DerbyLapTracker GUI and setup UI components."""
        EasyFrame.__init__(self, title="Derby Car Lap Time Tracker", width=900, height=700, resizable=False)

        # Configure grid layout rows, columns
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)

        # Load and display the logo image
        logo_path = "logo.png"
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((100, 100))
                self.logo = ImageTk.PhotoImage(image)
                self.addLabel(text="", row=0, column=0, columnspan=4)
                self.logo_label = Label(self, image=self.logo)
                self.logo_label.grid(row=0, column=0, columnspan=4, sticky="NSEW")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.addLabel(text=f"[Error: {e}]", row=0, column=0, columnspan=4, sticky="W")
        else:
            print("Logo image not found.")
            self.addLabel(text="[Logo Image Not Found]", row=0, column=0, columnspan=4, sticky="W")

        # Application description
        description = (
            "This application will track race data for two racers, one car each.\n"
            "After races are completed, and all data is manually entered (race times, lap numbers, race lane, etc),\n"
            "the program will output:\n"
            "- Fastest car on each lane\n"
            "- Average lap times for each car on each lane\n"
            "- Average lap times for each car on both lanes."
        )
        text_area = Text(self, wrap="word", height=9, width=60)
        text_area.insert("1.0", description)
        text_area.config(state=DISABLED)
        text_area.grid(row=1, column=0, columnspan=4, sticky="W")

        # Row 2: Inputs for number of racers and lanes
        self.addLabel(text="Number of Racers (max 2):", row=2, column=0, sticky="W")
        self.racerEntry = self.addTextField(text="", row=2, column=1)
        self.addLabel(text="Number of Lanes (max 2):", row=2, column=2, sticky="W")
        self.laneEntry = self.addTextField(text="", row=2, column=3)

        # Confirm button to validate and display racer detail fields
        self.addButton(text="Confirm", row=3, column=2, command=self.confirmAction)

        # Initialize racer count and store racer names
        self.racerCount = 0
        self.racer1Name = None  
        self.racer2Name = None  

    def confirmAction(self):
        """Validate racer and lane input values and create fields for racer details."""
        racers_text = self.racerEntry.getText().strip()
        lanes_text = self.laneEntry.getText().strip()

        try:
            racers = int(racers_text)
            lanes = int(lanes_text)
        except ValueError:
            self.messageBox("Error", "Please enter valid integer numbers for racers and lanes.")
            return
        
        if racers < 1 or racers > 2:
            self.messageBox("Error", "Number of racers must be 1 or 2.")
            return

        if lanes < 1 or lanes > 2:
            self.messageBox("Error", "Number of lanes must be 1 or 2.")
            return

        if hasattr(self, 'detailFieldsCreated'):
            return
        self.detailFieldsCreated = True

        self.addLabel(text="Racer Number (1 or 2):", row=4, column=0, sticky="W")
        self.racerNumberField = self.addTextField(text="", row=4, column=1)
        self.addLabel(text="Racer Name:", row=5, column=0, sticky="W")
        self.racerNameField = self.addTextField(text="", row=5, column=1)
        self.addLabel(text="Boy Scout Rank:", row=6, column=0, sticky="W")
        self.rankField = self.addTextField(text="", row=6, column=1)
        self.addLabel(text="Car Name:", row=7, column=0, sticky="W")
        self.carNameField = self.addTextField(text="", row=7, column=1)
        self.addLabel(text="Car Number (max 999):", row=8, column=0, sticky="W")
        self.carNumberField = self.addTextField(text="", row=8, column=1)
        self.addLabel(text="Car Weight:", row=9, column=0, sticky="W")
        self.carWeightField = self.addTextField(text="", row=9, column=1)
        self.addLabel(text="Mods:", row=10, column=0, sticky="W")
        self.modsArea = self.addTextArea(text="", row=10, column=1, width=50, height=8)

        self.saveRacerButton = self.addButton(text="Save Racer", row=11, column=0, columnspan=2, command=self.saveRacer)

    def saveRacer(self):
        """Saves racer data and ensures both racers are saved to the spreadsheet. File Explorer pop up asking user to name new file, or select existing file to record data"""
        try:
            racer_number = self.racerNumberField.getText().strip()
            racer_name = self.racerNameField.getText().strip()
            rank = self.rankField.getText().strip()
            car_name = self.carNameField.getText().strip()
            car_number = self.carNumberField.getText().strip()
            car_weight = self.carWeightField.getText().strip()
            mods = self.modsArea.get("1.0", "end").strip()

            # Ensure all fields are filled before saving
            if not racer_number or not racer_name or not car_name or not car_number or not car_weight:
                self.messageBox("Error", "All fields must be filled in before saving.")
                return

            # Store racer names for use in results display
            if racer_number == "1":
                self.racer1Name = racer_name
            elif racer_number == "2":
                self.racer2Name = racer_name

            # Create a DataFrame with racer details
            new_df = pd.DataFrame({
                "Racer Number": [racer_number],
                "Racer Name": [racer_name],
                "Boy Scout Rank": [rank],
                "Car Name": [car_name],
                "Car Number": [car_number],
                "Car Weight": [car_weight],
                "Mods": [mods]
            })

            # Ask user to choose a save location for the first time
            if not hasattr(self, "file_path") or not self.file_path:
                self.file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel Files", "*.xlsx")],
                    title="Choose a location to save race data"
                )

            # Ensure the user selected a valid file path
            if not self.file_path:
                self.messageBox("Error", "No file selected. Please select a file to save race data.")
                return

            # Check if the file exists, otherwise create it
            if not os.path.exists(self.file_path):
                # Create a new Excel file with an empty DataFrame
                with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="w") as writer:
                    new_df.to_excel(writer, sheet_name="Racer Details", index=False)

            else:
                # Load existing file
                try:
                    existing_df = pd.read_excel(self.file_path, sheet_name="Racer Details", engine="openpyxl")

                    # Ensure all required columns exist in the existing DataFrame
                    for col in ["Racer Number", "Racer Name", "Boy Scout Rank", "Car Name", "Car Number", "Car Weight", "Mods"]:
                        if col not in existing_df.columns:
                            existing_df[col] = ""

                    # Append new data
                    df = pd.concat([existing_df, new_df], ignore_index=True)

                except ValueError:
                    df = new_df  # If the sheet does not exist, create a new one

                # Save the updated DataFrame back to the Excel file
                with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                    df.to_excel(writer, sheet_name="Racer Details", index=False)

            self.messageBox("Success", f"Racer {racer_number} details saved successfully!")

            self.racerCount += 1  # Increment racer count

            if self.racerCount < 2:
                self.clearRacerFields()
                self.messageBox("Info", "Racer details saved. Enter the next racer's info.")
            else:
                self.messageBox("Info", "Maximum number of racers reached.")
                self.addButton(text="Enter Race Times", row=12, column=0, columnspan=2, command=self.openRaceEntryScreen)

        except Exception as e:
            self.messageBox("Error", f"Failed to save racer details: {e}")


    def saveRaceTime(self):
        """Saves race time data for 10 races to an Excel file."""
        try:
            race_data = {
                "Race #": [],
                "Racer 1 - Lane": [],
                "Racer 1 - Time": [],
                "Racer 2 - Lane": [],
                "Racer 2 - Time": []
            }

            # Collect race data from the input fields
            for i in range(10):  # Loop through 10 races
                race_data["Race #"].append(i + 1)
                race_data["Racer 1 - Lane"].append(int(self.laneFields1[i].getText().strip()))
                race_data["Racer 1 - Time"].append(float(self.timeFields1[i].getText().strip()))
                race_data["Racer 2 - Lane"].append(int(self.laneFields2[i].getText().strip()))
                race_data["Racer 2 - Time"].append(float(self.timeFields2[i].getText().strip()))

            new_df = pd.DataFrame(race_data)

            # Ask user to choose a save location for the first time
            if not hasattr(self, "file_path") or not self.file_path:
                self.file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel Files", "*.xlsx")],
                    title="Choose a location to save race data"
                )

            # Ensure the user selected a valid file path
            if not self.file_path:
                self.messageBox("Error", "No file selected. Please select a file to save race data.")
                return

            # Check if the file exists
            if os.path.exists(self.file_path):
                try:
                    # Load existing race time data
                    existing_df = pd.read_excel(self.file_path, sheet_name="Race Times", engine="openpyxl")

                    # Ensure all required columns exist
                    for col in ["Race #", "Racer 1 - Lane", "Racer 1 - Time", "Racer 2 - Lane", "Racer 2 - Time"]:
                        if col not in existing_df.columns:
                            existing_df[col] = ""

                    # Append new race data
                    df = pd.concat([existing_df, new_df], ignore_index=True)

                except ValueError:
                    # If the sheet does not exist, create it
                    df = new_df
            else:
                # If the file does not exist, create a new one
                df = new_df  

            # Save the updated DataFrame back to the Excel file
            with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name="Race Times", index=False)

            self.messageBox("Success", "Race times for 10 races saved successfully!")

        except Exception as e:
            self.messageBox("Error", f"Failed to save race times: {e}")

    def clearRacerFields(self):
        """Clears all racer input fields after saving."""
        self.racerNumberField.setText("")
        self.racerNameField.setText("")
        self.rankField.setText("")
        self.carNameField.setText("")
        self.carNumberField.setText("")
        self.carWeightField.setText("")
        self.modsArea.setText("")

    '''  Removed this so all racer 1 and 2 times would still be displayed when race times analyzed is showing
    def clearRaceFields(self):
        """Clears the race time and lane input fields in the race entry window."""
        for field in self.laneFields1:
            field.setText("")
        for field in self.laneFields2:
            field.setText("")
        for field in self.timeFields1:
            field.setText("")
        for field in self.timeFields2:
            field.setText("")'''


    def openRaceEntryScreen(self):
        """Opens a pop-up window for entering race times for both racers for 10 races, with properly aligned fields."""
        self.raceWindow = EasyFrame(title="Enter Race Times", width=1500, height=1150)

        # Headers - Ensure proper alignment
        self.raceWindow.addLabel(text="Race #", row=0, column=0, sticky="W")
        self.raceWindow.addLabel(text="Racer 1 - Lane", row=0, column=1, sticky="W")
        self.raceWindow.addLabel(text="Racer 1 - Time", row=0, column=2, sticky="W")
        self.raceWindow.addLabel(text="Racer 2 - Lane", row=0, column=3, sticky="W")
        self.raceWindow.addLabel(text="Racer 2 - Time", row=0, column=4, sticky="W")

        # Store input fields for later access
        self.laneFields1 = []
        self.timeFields1 = []
        self.laneFields2 = []
        self.timeFields2 = []

        for i in range(10):  # 10 races (starting row = 1)
            self.raceWindow.addLabel(text=f"Race {i + 1}:", row=i + 1, column=0, sticky="W")

            lane1 = self.raceWindow.addTextField(text="", row=i + 1, column=1)
            time1 = self.raceWindow.addTextField(text="", row=i + 1, column=2)
            lane2 = self.raceWindow.addTextField(text="", row=i + 1, column=3)
            time2 = self.raceWindow.addTextField(text="", row=i + 1, column=4)

            self.laneFields1.append(lane1)
            self.timeFields1.append(time1)
            self.laneFields2.append(lane2)
            self.timeFields2.append(time2)

        # Buttons
        self.raceWindow.addButton(text="Save Race Times", row=11, column=0, columnspan=5, command=self.saveRaceTime)
        self.raceWindow.addButton(text="Analyze Race Results", row=12, column=0, columnspan=5, command=self.analyzeRaceResults)

        
    def analyzeRaceResults(self):
        """Analyzes race results to determine fastest cars and average race times."""
        file_path = r"C:\Users\Zeke\Documents\derby_car_program.xlsx"

        if not os.path.exists(file_path):
            self.messageBox("Error", "Race results file not found.")
            return

        try:
            # Read racer details
            racer_df = pd.read_excel(file_path, sheet_name="Racer Details", engine="openpyxl")
            racer_dict = dict(zip(racer_df["Racer Number"].astype(str), racer_df["Racer Name"]))

            # Assign racer names dynamically
            self.racer1Name = racer_dict.get("1", "Racer 1")
            self.racer2Name = racer_dict.get("2", "Racer 2")

            # Read race times
            df = pd.read_excel(file_path, sheet_name="Race Times", engine="openpyxl")
            df.columns = df.columns.str.strip()

            # Convert race times and lane numbers to numeric values
            df["Racer 1 - Time"] = pd.to_numeric(df["Racer 1 - Time"], errors="coerce")
            df["Racer 2 - Time"] = pd.to_numeric(df["Racer 2 - Time"], errors="coerce")
            df["Racer 1 - Lane"] = pd.to_numeric(df["Racer 1 - Lane"], errors="coerce").astype("Int64")
            df["Racer 2 - Lane"] = pd.to_numeric(df["Racer 2 - Lane"], errors="coerce").astype("Int64")

            df.fillna(0, inplace=True)  # Replace NaN values with 0

            # Find the fastest times and the corresponding racers
            fastest_lane_1_time = df[df["Racer 1 - Lane"] == 1]["Racer 1 - Time"].min(skipna=True)
            fastest_lane_2_time = df[df["Racer 2 - Lane"] == 2]["Racer 2 - Time"].min(skipna=True)

            fastest_lane_1_racer = self.racer1Name if (df["Racer 1 - Time"] == fastest_lane_1_time).any() else self.racer2Name
            fastest_lane_2_racer = self.racer2Name if (df["Racer 2 - Time"] == fastest_lane_2_time).any() else self.racer1Name

            # Average times per racer per lane
            avg_racer1_lane1 = df[df["Racer 1 - Lane"] == 1]["Racer 1 - Time"].mean(skipna=True)
            avg_racer1_lane2 = df[df["Racer 1 - Lane"] == 2]["Racer 1 - Time"].mean(skipna=True)
            avg_racer2_lane1 = df[df["Racer 2 - Lane"] == 1]["Racer 2 - Time"].mean(skipna=True)
            avg_racer2_lane2 = df[df["Racer 2 - Lane"] == 2]["Racer 2 - Time"].mean(skipna=True)

            # Overall averages per racer
            avg_racer1 = df["Racer 1 - Time"].mean(skipna=True)
            avg_racer2 = df["Racer 2 - Time"].mean(skipna=True)

            # Format NaN values
            def format_time(value):
                return f"{value:.2f} seconds" if not pd.isna(value) else "0.00 seconds"

            results_text = (
                f"Fastest Car on Lane 1: {fastest_lane_1_racer}, {format_time(fastest_lane_1_time)}\n"
                f"Fastest Car on Lane 2: {fastest_lane_2_racer}, {format_time(fastest_lane_2_time)}\n\n"
                f"Average Race Time for {self.racer1Name} on Lane 1: {format_time(avg_racer1_lane1)}\n"
                f"Average Race Time for {self.racer1Name} on Lane 2: {format_time(avg_racer1_lane2)}\n"
                f"Average Race Time for {self.racer2Name} on Lane 1: {format_time(avg_racer2_lane1)}\n"
                f"Average Race Time for {self.racer2Name} on Lane 2: {format_time(avg_racer2_lane2)}\n\n"
                f"Overall Average Race Time for {self.racer1Name}: {format_time(avg_racer1)}\n"
                f"Overall Average Race Time for {self.racer2Name}: {format_time(avg_racer2)}"
            )

            # Display results
            results_window = EasyFrame(title="Race Results", width=1500, height=1500)
            results_window.addLabel(text="Race Results", row=0, column=0, sticky="NSEW")
            
            text_area = results_window.addTextArea(text=results_text, row=1, column=0, width=70, height=20)
            text_area.config(state=DISABLED)

            results_window.addButton(text="Close", row=2, column=0, command=results_window.destroy)

        except Exception as e:
            self.messageBox("Error", f"Failed to analyze race results: {e}")

if __name__ == "__main__":
    DerbyLapTracker().mainloop()
