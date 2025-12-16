from capture import PacketCapture
import time
from urllib.request import urlopen

from protos import _PacketCommand_pb2
from protos import _Defins_pb2

pc = _PacketCommand_pb2.PacketCommand


build_version_url = "http://cdn.darkanddarker.com/Dark%20and%20Darker/Build/BuildVersion.txt"

with urlopen(build_version_url) as f:
    build_version = f.read().decode("utf-8").strip()

print(f"Build Version: {build_version}")

def save(message):
    with open("output.txt", "a") as file:
        file.write(str(message) + "\n")

def show(message):
    from google.protobuf.json_format import MessageToJson
    json_str = MessageToJson(message, always_print_fields_with_no_presence=True)
    print(json_str)

def policy(message):
    text = ""
    for policy in message.policyList:
        name = _Defins_pb2.Operate.Policy.Name(policy.policyType)
        text += f"{name or 'UnknownPolicy'}: {getattr(policy, 'policyValue', 'N/A')}\n"
    
    with open(f"S2C_SERVICE_POLICY_NOT_{build_version}.txt", "w") as file:
        file.write(text)


def main():
    capture_info = {
        pc.S2C_SERVICE_POLICY_NOT: policy, # save policy list
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
