from capture import DarkandDarkerCapture
from google.protobuf.json_format import MessageToJson
from datetime import datetime
import os

def save(capture, message, name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    dir_path = f"data/{name}"
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{timestamp}.txt")

    with open(file_path, "w") as file:
        json_str = MessageToJson(message, always_print_fields_with_no_presence=True)
        file.write(json_str)

def show(capture, message, name):
    json_str = MessageToJson(message, always_print_fields_with_no_presence=True)
    print(json_str)

def main():
    # Network interface used for packet capture (change as needed)
    INTERFACE = "Ethernet"
    dc = DarkandDarkerCapture(INTERFACE)

    # Setup capture to save all packets
    for command_name in dc.pc.keys():
        dc.capture_info[command_name] = save

    # Run continuous capture
    dc.capture()


if __name__ == "__main__":
    main()
