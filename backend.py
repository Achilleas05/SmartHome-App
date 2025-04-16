# Task 1
class SmartPlug:
    def __init__(self, consumption_rate):
        if not (isinstance(consumption_rate, int) and 0 <= consumption_rate <= 150):
            raise ValueError(
                f"Invalid consumption rate: {consumption_rate}. Must be an integer between 0 and 150."
            )
        self._switched_on = False
        self._consumption_rate = consumption_rate

    def toggle_switch(self):
        self._switched_on = not self._switched_on

    @property
    def consumption_rate(self):
        return self._consumption_rate

    @consumption_rate.setter
    def consumption_rate(self, consumption_rate):
        if not (isinstance(consumption_rate, int) and 0 <= consumption_rate <= 150):
            raise ValueError(
                f"Invalid consumption rate: {consumption_rate}. Must be an integer between 0 and 150."
            )
        self._consumption_rate = consumption_rate

    def __str__(self):
        if self._switched_on:
            return (
                f"SmartPlug is on with a consumption rate of {self._consumption_rate}"
            )
        return f"SmartPlug is off with a consumption rate of {self._consumption_rate}"


def test_smart_plug():
    print("Testing valid inputs:")
    plug = SmartPlug(45)
    print(plug)

    plug.toggle_switch()
    print("After toggling switch:")
    print(plug)

    plug.consumption_rate = 75
    print("After updating consumption rate:")
    print(plug)

    plug.toggle_switch()
    print("After toggling switch again:")
    print(plug)

    print("\nTesting invalid inputs:")
    try:
        plug.consumption_rate = 200
    except ValueError as e:
        print(f"Error: {e}")
        print("Current consumption rate:", plug.consumption_rate)  # Should still be 75

    try:
        invalid_plug = SmartPlug(-10)
    except ValueError as e:
        print(f"Error: {e}")


# test_smart_plug()


# Task 2
class Device:
    def __init__(self):
        self._switched_on = False

    def toggle_switch(self):
        self._switched_on = not self._switched_on


class SmartTV(Device):
    def __init__(self):
        super().__init__()
        self._channel = 1

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, new_channel):
        if not (isinstance(new_channel, int) and 1 <= new_channel <= 734):
            raise ValueError(
                f"Invalid channel: {new_channel}. Must be an integer between 1 and 734."
            )
        self._channel = new_channel

    def __str__(self):
        if self._switched_on:
            return f"SmartTV is on with channel {self._channel}"
        return f"SmartTV is off with channel {self._channel}"


class SmartSpeaker(Device):
    def __init__(self):
        super().__init__()
        self._streaming = "Amazon"

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    def streaming(self, new_streaming):
        if new_streaming not in ["Amazon", "Apple", "Spotify"]:
            raise ValueError(
                f"Invalid streaming service: {new_streaming}. Must be Amazon, Apple, or Spotify."
            )
        self._streaming = new_streaming

    def __str__(self):
        status = "on" if self._switched_on else "off"
        return f"SmartSpeaker is {status} with streaming service {self._streaming}"


def test_custom_devices():
    tv = SmartTV()
    speaker = SmartSpeaker()

    print(tv)
    print(speaker)

    # Toggle switches
    tv.toggle_switch()
    speaker.toggle_switch()
    print(tv)
    print(speaker)

    # Update attributes
    tv.channel = 100
    speaker.streaming = "Spotify"
    print(tv)
    print(speaker)

    try:
        tv.channel = 800
    except ValueError as e:
        print(f"Error: {e}")

    try:
        speaker.streaming = "Netflix"
    except ValueError as e:
        print(f"Error: {e}")


# test_custom_devices()


# Task 3
class SmartHome:
    def __init__(self, max_items=10):
        self._devices = []
        self._max_items = max_items

    def add_device(self, device):
        if len(self._devices) < self._max_items:
            self._devices.append(device)
        else:
            raise ValueError("Cannot add more devices: maximum limit reached.")

    def get_device(self, index):
        if 0 <= index < len(self._devices):
            return self._devices[index]
        else:
            raise IndexError("Invalid device index.")

    def toggle_device(self, index):
        if 0 <= index < len(self._devices):
            self._devices[index].toggle_switch()
        else:
            raise IndexError("Invalid device index.")

    def switch_all_on(self):
        for device in self._devices:
            if not device._switched_on:
                device.toggle_switch()

    def switch_all_off(self):
        for device in self._devices:
            if device._switched_on:
                device.toggle_switch()

    def remove_device(self, index):
        if 0 <= index < len(self._devices):
            self._devices.pop(index)  # Remove the device at the specified index
        else:
            raise IndexError("Invalid device index.")

    def __str__(self):
        output = f"SmartHome with {len(self._devices)} device(s):\n"
        i = 1  # Start counting from 1
        for device in self._devices:
            output += f"{i}- {device}\n"
            i += 1
        return output


def test_smart_home():
    smart_home = SmartHome()

    smart_plug = SmartPlug(45)
    smart_tv = SmartTV()
    smart_speaker = SmartSpeaker()

    smart_home.add_device(smart_plug)
    smart_home.add_device(smart_tv)
    smart_home.add_device(smart_speaker)

    print("Initial SmartHome state:")
    print(smart_home)

    smart_home.toggle_device(0)
    smart_home.toggle_device(1)
    smart_home.toggle_device(2)

    print("\nAfter toggling devices:")
    print(smart_home)

    # Update device attributes
    smart_tv.channel = 100
    smart_speaker.streaming = "Spotify"

    print("\nAfter updating attributes:")
    print(smart_home)

    smart_home.remove_device(0)
    print("\nAfter removing SmartPlug:")
    print(smart_home)

    try:
        smart_home.remove_device(10)
    except IndexError as e:
        print(f"\nError: {e}")

    try:
        smart_home.add_device(SmartPlug(50))
        smart_home.add_device(SmartPlug(60))
    except ValueError as e:
        print(f"\nError: {e}")


# test_smart_home()
