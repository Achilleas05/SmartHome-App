import csv
from tkinter import Tk, Frame, Label, Button, Toplevel, StringVar, Entry
from backend import SmartHome, SmartPlug, SmartTV, SmartSpeaker

class SmartHomesApp:
    def __init__(self):
        self.homes = []  # List of SmartHome objects
        self.current_home_index = None  # Tracks which home is active

        self.win = Tk()
        self.win.title("Smart Homes Manager")

        self.main_frame = Frame(self.win)
        self.main_frame.pack(fill="both", padx=10, pady=10)

        # Initialize the list to track widgets in the device frame
        self.device_widgets = []

        self.create_widgets()

        # Load saved homes when the app starts
        self.load_homes()

    def create_widgets(self):
        Button(self.main_frame, width=20, text="Add Home", command=self.add_home
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        Button(
            self.main_frame, width=20, text="Remove Home", command=self.remove_home
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        Button(
            self.main_frame, width=20, text="Switch Home", command=self.switch_home
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Label to display the current home
        self.home_label = Label(self.main_frame, text="No home selected")
        self.home_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Frame to display devices in the current home
        self.device_frame = Frame(self.main_frame)
        self.device_frame.grid(row=2, column=0, columnspan=3, pady=10)

    def add_home(self):
        new_home = SmartHome()
        self.homes.append(new_home)
        self.current_home_index = len(self.homes) - 1  # Set index to the last added home
        self.update_home_label()
        self.refresh_ui()
        self.save_homes()

    def remove_home(self):
        if self.current_home_index is not None and len(self.homes) > 0:
            self.homes.pop(self.current_home_index)  # Remove home
            if len(self.homes) == 0:
                self.current_home_index = None
            else:
                self.current_home_index = 0  # Select another home if available
            self.update_home_label()
            self.refresh_ui()
            self.save_homes()

    def switch_home(self):
        if len(self.homes) > 0:
            # Move to the next home, reset to 0 if at the end
            self.current_home_index += 1
            if self.current_home_index >= len(self.homes):
                self.current_home_index = 0
            self.update_home_label()
            self.refresh_ui()

    def update_home_label(self):
        if self.current_home_index is None:
            self.home_label["text"] = "No home selected"
        else:
            self.home_label["text"] = f"Home {self.current_home_index + 1}"  # Show home numbers starting from 1

    def refresh_ui(self):
        # Clear existing widgets in the device frame
        for widget in self.device_widgets:
            widget.destroy()
        self.device_widgets.clear()  # Reset the list

        row = 0

        if self.current_home_index is not None:
            home = self.homes[self.current_home_index]
            for i in range(len(home._devices)):  
                device = home._devices[i]
                status = "on" if device._switched_on else "off"

                # Determine device type and attributes
                if isinstance(device, SmartPlug):
                    attribute = f"Consumption: {device.consumption_rate}W"
                    name = "Plug"
                elif isinstance(device, SmartTV):
                    attribute = f"Channel: {device.channel}"
                    name = "TV"
                elif isinstance(device, SmartSpeaker):
                    attribute = f"Streaming: {device.streaming}"
                    name = "Speaker"

                # Display device information
                device_label = Label(self.device_frame, text=f"{name} is {status}, {attribute}")
                device_label.grid(row=row, column=0, sticky="w")
                self.device_widgets.append(device_label)  # Track the widget

                # Buttons to control individual devices
                toggle_button = Button(
                    self.device_frame,
                    width=10,
                    text="Toggle",
                    command=lambda i=i: self.toggle_device(i)
                )
                toggle_button.grid(row=row, column=1, padx=(10, 0), pady=5, sticky="w")
                self.device_widgets.append(toggle_button)  # Track the widget

                edit_button = Button(
                    self.device_frame,
                     width=5,
                    text="Edit",
                    command=lambda i=i: self.edit_device(i)
                )
                edit_button.grid(row=row, column=2, sticky="w")
                self.device_widgets.append(edit_button)  # Track the widget

                delete_button = Button(
                    self.device_frame,
                    width=10,
                    text="Delete",
                    command=lambda i=i: self.delete_device(i)
                )
                delete_button.grid(row=row, column=3, sticky="w")
                self.device_widgets.append(delete_button)  # Track the widget

                row += 1

            # Display summary information
            num_devices = len(home._devices)
            num_on = 0
            for device in home._devices:
                if device._switched_on:
                    num_on += 1
        
            summary_label = Label(self.device_frame, text=f"Devices: {num_devices}, On: {num_on}")
            summary_label.grid(row=row, column=0, columnspan=4, pady=10)
            self.device_widgets.append(summary_label)  # Track the widget

            row += 1

        # Button to add a new device
        add_device_button = Button(self.device_frame, text="Add Device", command=self.add_device)
        add_device_button.grid(row=row, column=0, columnspan=4, pady=10)
        self.device_widgets.append(add_device_button)  # Track the widget
    
    def add_device(self):
        if self.current_home_index is not None:
            add_window = Toplevel(self.win)
            add_window.title("Add Device")

            Label(add_window, text="Select Device Type:").grid(row=0, column=0)

            Button(
                add_window,
                width=10,
                text="SmartPlug",
                command=lambda: self.setup_device(SmartPlug(0), add_window)
            ).grid(row=1, column=0, pady=5)
            
            Button(
                add_window,
                width=10,
                text="SmartTV",
                command=lambda: self.setup_device(SmartTV(), add_window)
            ).grid(row=2, column=0, pady=5)
            
            Button(
                add_window,
                width=10,
                text="SmartSpeaker",
                command=lambda: self.setup_device(SmartSpeaker(), add_window)
            ).grid(row=3, column=0, pady=5)

    def setup_device(self, device, add_window):
        add_window.destroy()
        setup_window = Toplevel(self.win)
        setup_window.title("Setup Device")

        channel_var = StringVar()
        streaming_var = StringVar()
        consumption_var = StringVar()

        if isinstance(device, SmartPlug):
            Label(setup_window, text="Consumption Rate:").grid(row=0, column=0)
            consumption_var.set(device.consumption_rate)
            Entry(setup_window, textvariable=consumption_var).grid(row=0, column=1)
        elif isinstance(device, SmartTV):
            Label(setup_window, text="Channel:").grid(row=0, column=0)
            channel_var.set(device.channel)
            Entry(setup_window, textvariable=channel_var).grid(row=0, column=1)
        elif isinstance(device, SmartSpeaker):
            Label(setup_window, text="Streaming:").grid(row=0, column=0)
            streaming_var.set(device.streaming)
            Entry(setup_window, textvariable=streaming_var).grid(row=0, column=1)

        Button(
            setup_window,
            text="Confirm",
            command=lambda: self.apply_changes(device, channel_var, streaming_var, consumption_var, setup_window)
        ).grid(row=1, columnspan=2)

    def edit_device(self, index):
        device = self.homes[self.current_home_index]._devices[index]
        edit_window = Toplevel(self.win)
        edit_window.title("Edit Device")

        channel_var = StringVar()
        streaming_var = StringVar()
        consumption_var = StringVar()

        if isinstance(device, SmartPlug):
            Label(edit_window, text="Consumption Rate:").grid(row=0, column=0)
            consumption_var.set(device.consumption_rate)
            Entry(edit_window, textvariable=consumption_var).grid(row=0, column=1)
        elif isinstance(device, SmartTV):
            Label(edit_window, text="Channel:").grid(row=0, column=0)
            channel_var.set(device.channel)
            Entry(edit_window, textvariable=channel_var).grid(row=0, column=1)
        elif isinstance(device, SmartSpeaker):
            Label(edit_window, text="Streaming:").grid(row=0, column=0)
            streaming_var.set(device.streaming)
            Entry(edit_window, textvariable=streaming_var).grid(row=0, column=1)

        Button(
            edit_window,
            text="Confirm",
            command=lambda: self.apply_changes(device, channel_var, streaming_var, consumption_var, edit_window, is_add=False)
        ).grid(row=1, columnspan=2)

    def apply_changes(self, device, channel_var, streaming_var, consumption_var, window, is_add=True):
        try:
            if isinstance(device, SmartPlug):
                new_consumption = int(consumption_var.get())
                if not (0 <= new_consumption <= 150):
                    raise ValueError("Consumption rate must be between 0 and 150.")
                device.consumption_rate = new_consumption
            elif isinstance(device, SmartTV):
                new_channel = int(channel_var.get())
                if not (1 <= new_channel <= 734):
                    raise ValueError("Channel must be between 1 and 734.")
                device.channel = new_channel
            elif isinstance(device, SmartSpeaker):
                streaming_value = streaming_var.get().strip().lower()
                if streaming_value not in ["amazon", "apple", "spotify"]:
                    raise ValueError("Streaming must be Amazon, Apple, or Spotify.")
                device.streaming = streaming_value.capitalize()

            if is_add:
                self.homes[self.current_home_index].add_device(device)

            window.destroy()
            self.refresh_ui()
            self.save_homes()
        except ValueError as e:
            error_window = Toplevel(self.win)
            error_window.title("Error")
            Label(error_window, text=str(e)).pack(pady=10)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def toggle_device(self, index):
        try:
            self.homes[self.current_home_index].toggle_device(index)
            self.refresh_ui()
            self.save_homes()
        except IndexError:
            error_window = Toplevel(self.win)
            error_window.title("Error")
            Label(error_window, text="Invalid device index.").pack(pady=10)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def delete_device(self, index):
        try:
            self.homes[self.current_home_index].remove_device(index)
            self.refresh_ui()
            self.save_homes()
        except IndexError:
            error_window = Toplevel(self.win)
            error_window.title("Error")
            Label(error_window, text="Invalid device index.").pack(pady=10)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def save_homes(self):
        with open("smart_homes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            home_index = 0  # Initialize a counter for the home index
            for home in self.homes:  # Loop through each home
                for device in home._devices:
                    if isinstance(device, SmartPlug):
                        writer.writerow([home_index, "SmartPlug", device._switched_on, device.consumption_rate])
                    elif isinstance(device, SmartTV):
                        writer.writerow([home_index, "SmartTV", device._switched_on, device.channel])
                    elif isinstance(device, SmartSpeaker):
                        writer.writerow([home_index, "SmartSpeaker", device._switched_on, device.streaming])
                home_index += 1  # Increment the home index for the next home

    def load_homes(self):
        try:
            with open("smart_homes.csv", "r") as file:
                reader = csv.reader(file)
                self.homes = []  # Reset the list of homes
                for row in reader:
                    if len(row) >= 4:  # Ensure the row has enough columns
                        home_index, device_type, switched_on, attribute = row
                        home_index = int(home_index)
                        switched_on = switched_on == "True"

                    # Ensure we have enough homes
                        while len(self.homes) <= home_index:
                            self.homes.append(SmartHome())

                    # Create the device and add it to the correct home
                        if device_type == "SmartPlug":
                            device = SmartPlug(int(attribute))
                            device._switched_on = switched_on
                        elif device_type == "SmartTV":
                            device = SmartTV()
                            device._switched_on = switched_on
                            device.channel = int(attribute)
                        elif device_type == "SmartSpeaker":
                            device = SmartSpeaker()
                            device._switched_on = switched_on
                            device.streaming = attribute

                        self.homes[home_index].add_device(device)

            # Set the current home index to 0 if there are homes
                if self.homes:
                    self.current_home_index = 0
                else:
                    self.current_home_index = None

                self.update_home_label()
                self.refresh_ui()
        except FileNotFoundError:
            pass

    def run(self):
        self.win.mainloop()

def test_smart_homes_app():
    app = SmartHomesApp()
    app.run()

test_smart_homes_app()