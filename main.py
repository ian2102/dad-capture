from capture import PacketCapture
import time

from protos import _PacketCommand_pb2
from protos import _Defins_pb2

pc = _PacketCommand_pb2.PacketCommand


def save(message):
    with open("output.txt", "a") as file:
        file.write(str(message) + "\n")

def show(message):
    from google.protobuf.json_format import MessageToJson
    json_str = MessageToJson(message, always_print_fields_with_no_presence=True)
    print(json_str)

def main():
    capture_info = {
    }

    # save all packets to output.txt
    for value in pc.values():
        capture_info[value] = save

    capture = PacketCapture(capture_info)

    capture.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        capture.stop()

if __name__ == "__main__":
    main()
