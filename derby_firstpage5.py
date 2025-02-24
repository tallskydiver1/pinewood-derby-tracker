from breezypythongui import EasyFrame
from tkinter import Label, Text, DISABLED
import os
from PIL import Image, ImageTk
import tkinter as tk

class DerbyLapTracker(EasyFrame):
    def __init__(self):
        # Increase width and height to allow extra fields later.
        EasyFrame.__init__(self, title="Derby Car Lap Time Tracker", width=900, height=700, resizable=False)
        
        # Configure each grid column with equal weight.
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        
        # Load and display the logo image.
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
            print("Logo image not found. Ensure 'logo.png' is in the same directory as the script.")
            self.addLabel(text="[Logo Image Not Found]", row=0, column=0, columnspan=4, sticky="W")
        
        # Application description.
        description = (
            "This application will track race data for two racers, one car each.\n"
            "After races are completed, and all data is manually entered (race times, lap numbers, etc),\n"
            "the program will output:\n"
            "- Fastest car on each lane\n"
            "- Average lap times for each car on each lane\n"
            "- Average lap times for each car on both lanes."
        )
        text_area = Text(self, wrap="word", height=9, width=60)
        text_area.insert("1.0", description)
        text_area.config(state=DISABLED)
        text_area.grid(row=1, column=0, columnspan=4, sticky="W")
        
        # Row 2: Labels and entry fields for number of racers and lanes.
        self.addLabel(text="Number of Racers (max 2):", row=2, column=0, sticky="W")
        self.racerEntry = self.addTextField(text="", row=2, column=1)
        self.racerEntry.grid_configure(sticky="W")
        
        self.addLabel(text="Number of Lanes (max 2):", row=2, column=2, sticky="W")
        self.laneEntry = self.addTextField(text="", row=2, column=3)
        self.laneEntry.grid_configure(sticky="W")
        
        # Confirm button (placed in row 3, column 2)
        self.addButton(text="Confirm", row=3, column=2, command=self.confirmAction)
        
        # Force the layout to update immediately.
        self.update()
        
    def confirmAction(self):
        # Retrieve and validate the number of racers and lanes.
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
        
        # Proceed to display additional detail fields if not already created.
        if hasattr(self, 'detailFieldsCreated'):
            return  # Avoid duplicating fields if confirm is pressed again.
        self.detailFieldsCreated = True
        
        currentRow = 4  # Start adding detail fields from row 4.
        
        self.addLabel(text="Racer Details Entry:", row=currentRow, column=0, columnspan=4, sticky="W")
        currentRow += 1
        
        self.addLabel(text="Racer Number (1 or 2):", row=currentRow, column=0, sticky="W")
        self.racerNumberField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        self.addLabel(text="Racer Name:", row=currentRow, column=0, sticky="W")
        self.racerNameField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        self.addLabel(text="Boy Scout Rank:", row=currentRow, column=0, sticky="W")
        self.rankField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        self.addLabel(text="Car Name:", row=currentRow, column=0, sticky="W")
        self.carNameField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        self.addLabel(text="Car Number (max 999):", row=currentRow, column=0, sticky="W")
        self.carNumberField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        self.addLabel(text="Car Weight:", row=currentRow, column=0, sticky="W")
        self.carWeightField = self.addTextField(text="", row=currentRow, column=1)
        currentRow += 1
        
        # Place the mods label on its own row.
        self.addLabel(text="Mods-enter details, up to 4 lines ([canted wheels front/back/degree],[polished axles],\n[3 wheel rail rider], etc):", row=currentRow, column=0, columnspan=2, sticky="W")
        currentRow += 1
        self.modsArea = self.addTextArea(text="", row=currentRow, column=0, columnspan=2, width=50, height=4)
        currentRow += 1
        
        self.messageBox("Info", "Please enter the details for the racer.")
        
    '''def open_child1(self):
        # Create a child window relative to this EasyFrame instance.
        child1_window = tk.Toplevel(self)
        child1_window.title("Confirm Racer, Car, Mods Info Entry")
        tk.Label(child1_window, text="This is a child window").pack()
        tk.Button(child1_window, text="Close", command=child1_window.destroy).pack()'''
        
if __name__ == "__main__":
    DerbyLapTracker().mainloop()
