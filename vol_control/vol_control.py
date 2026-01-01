from gpiozero import Button
import subprocess
import time

# GPIO pins for your buttons
up_button = Button(23)
down_button = Button(24)
mute_button = Button(25)  # change to the GPIO pin you wire for mute

# Step size for volume change (in %)
step = 5

# Track mute state
is_muted = False

# Function to get current PCM volume
def get_volume():
    result = subprocess.run(["amixer", "get", "PCM"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Playback" in line and "%" in line:
            vol = int(line.split("[")[1].split("%")[0])
            return vol
    return 50  # default if parsing fails

# Function to set PCM volume
def set_volume(vol):
    vol = max(0, min(100, vol))  # clamp between 0 and 100
    subprocess.run(["amixer", "set", "PCM", f"{vol}%"])
    print(f"Volume set to {vol}%")

# Function to toggle mute
def toggle_mute():
    global is_muted
    is_muted = not is_muted
    subprocess.run(["amixer", "set", "PCM", "mute" if is_muted else "unmute"])
    print("Muted" if is_muted else "Unmuted")

# Callback functions
def volume_up():
    if not is_muted:
        vol = get_volume() + step
        set_volume(vol)

def volume_down():
    if not is_muted:
        vol = get_volume() - step
        set_volume(vol)

# Attach callbacks
up_button.when_pressed = volume_up
down_button.when_pressed = volume_down
mute_button.when_pressed = toggle_mute

print("Volume control running. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting volume control.")

