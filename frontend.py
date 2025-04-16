from tkinter import Tk, Frame, Label, Button, Toplevel, StringVar, Entry
from backend import SmartHome, SmartPlug, SmartTV, SmartSpeaker


class SmartHomeApp:
    def __init__(self, smart_home):
        self.smart_home = smart_home
        self.win = Tk()
        self.win.title("Smart Home App")

        self.main_frame = Frame(self.win)
        self.main_frame.pack(fill="both", padx=10, pady=10)

        self.device_widgets = []

        self.create_widgets()

        self.btn_add = Button(self.main_frame, width=5, text="Add", command=self.add)
        self.btn_add.grid(column=0, row=1000, pady=10, sticky="w")

    def create_widgets(self):
        Button(
            self.main_frame, width=20, text="Turn off all", command=self.turn_all_off
        ).grid(column=1, columnspan=2, row=0, padx=10, pady=5, sticky="ew")
        
        Button(
            self.main_frame, width=20, text="Turn on all", command=self.turn_all_on
        ).grid(column=0, row=0, pady=5, sticky="w")


        # Loop through each device and create its UI elements
        row = 1
        for device in self.smart_home._devices:
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
            device_label = Label(self.main_frame, text=f"{name} is {status}, {attribute}")
            device_label.grid(row=row, column=0, sticky="w")

            # Buttons to control individual devices
            toggle_button = Button(
                self.main_frame,
                width=10,
                text="Toggle",
                command=lambda i=row - 1: self.toggle_device(i),  # Creates a small function that only runs when the button is clicked
            )
            toggle_button.grid(row=row, column=1, padx=(10, 0), pady=5, sticky="w")

            edit_button = Button(
                self.main_frame,
                width=5,
                text="Edit",
                command=lambda i=row - 1: self.edit_device(i),
            )
            edit_button.grid(row=row, column=2, sticky="w")

            delete_button = Button(
                self.main_frame,
                width=10,
                text="Delete",
                command=lambda i=row - 1: self.delete_device(i),
            )
            delete_button.grid(row=row, column=3, sticky="w")

            # Store widget references for later updates
            self.device_widgets.append(
                (device_label, toggle_button, edit_button, delete_button)
            )
            row += 1

    def toggle_device(self, index):
        self.smart_home.toggle_device(index)
        self.refresh_ui()

    def turn_all_on(self):
        self.smart_home.switch_all_on()
        self.refresh_ui()

    def turn_all_off(self):
        self.smart_home.switch_all_off()
        self.refresh_ui()

    def delete_device(self, index):
        self.smart_home.remove_device(index)
        self.refresh_ui()

    def add(self):
        add_window = Toplevel(self.win)
        add_window.title("Add Device")

        Label(add_window, text="Select Device Type:").grid(row=0, column=0)

        Button(
            add_window,
            width=10,
            text="SmartPlug",
            command=lambda: self.setup_device(SmartPlug(0), add_window),
        ).grid(row=1, column=0, pady=5)
        
        Button(
            add_window,
            width=10,
            text="SmartTV",
            command=lambda: self.setup_device(SmartTV(), add_window),
        ).grid(row=2, column=0, pady=5)
        
        Button(
            add_window,
            width=10,
            text="SmartSpeaker",
            command=lambda: self.setup_device(SmartSpeaker(), add_window),
        ).grid(row=3, column=0, pady=5)

    def setup_device(self, device, add_window):
        # Close the "Add Device" window
        add_window.destroy()

        setup_window = Toplevel(self.win)
        setup_window.title("Setup Device")

        # Variables to store user input
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

        # Button to confirm the configuration
        Button(
            setup_window,
            text="Confirm",
            command=lambda: self.apply_changes(device, channel_var, streaming_var, consumption_var, setup_window),
        ).grid(row=1, columnspan=2)

    def edit_device(self, index):
        device = self.smart_home._devices[index]
        edit_window = Toplevel(self.win)
        edit_window.title("Edit Device")

        channel_var = StringVar()
        streaming_var = StringVar()
        consumption_var = StringVar()

        if isinstance(device, SmartPlug):
            Label(edit_window, text="Consumption Rate:").grid(row=0, column=0)
            consumption_var.set(device.consumption_rate)  # Pre-fills the input box with the device’s current consumption rate.
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
            command=lambda: self.apply_changes(
                device,
                channel_var,
                streaming_var,
                consumption_var,
                edit_window,
                is_add=False,  # Tells apply_changes() that this is an edit, not a new device.
            ),
        ).grid(row=1, columnspan=2)

    def apply_changes(self, device, channel_var, streaming_var, consumption_var, window, is_add=True):  # Default value, meaning if not specified, assume it's adding a new device.
        try:
            if isinstance(device, SmartPlug):
                try:
                    new_consumption = int(consumption_var.get())
                except ValueError:
                    raise ValueError("Consumption rate must be a number.")
                if not (0 <= new_consumption <= 150):
                    raise ValueError("Consumption rate must be between 0 and 150.")
                device.consumption_rate = new_consumption
            elif isinstance(device, SmartTV):
                try:
                    new_channel = int(channel_var.get())
                except ValueError:
                    raise ValueError("Channel must be a number.")
                if not (1 <= new_channel <= 734):
                    raise ValueError("Channel must be between 1 and 734.")
                device.channel = new_channel
            elif isinstance(device, SmartSpeaker):
                streaming_value = streaming_var.get().strip().lower()  # Converts it to lowercase for comparison.
                valid_streaming_services = ["amazon", "apple", "spotify"]
                if streaming_value not in valid_streaming_services:
                    raise ValueError("Streaming must be Amazon, Apple, or Spotify.")
                device.streaming = streaming_value.capitalize()

            # Add the device if it's new
            if is_add:
                self.smart_home.add_device(device)

            # Close the setup window
            window.destroy()

            # Refresh the UI to show the updated device list
            self.refresh_ui()
        except ValueError as e:
            # Show an error message if something goes wrong
            error_window = Toplevel(self.win)
            error_window.title("Error")
            Label(error_window, text=str(e)).pack(pady=10)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def refresh_ui(self):
        # Clear existing widgets (except the "Add" button)
        for widget in self.device_widgets:
            for i in widget:
                i.destroy()
        self.device_widgets.clear()

        # Recreate widgets (except the "Add" button)
        self.create_widgets()

    def run(self):
        self.win.mainloop()


def test_smart_home_system():
    smart_home = SmartHome()
    smart_home.add_device(SmartTV())
    smart_home.add_device(SmartSpeaker())
    smart_home.add_device(SmartPlug(45))

    app = SmartHomeApp(smart_home)
    app.run()


test_smart_home_system()
