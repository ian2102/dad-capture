import os
import sys
import pyshark
import struct
import importlib.util

class DarkandDarkerCapture:
    def __init__(self, interface):
        self.interface = interface

        # Determine paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.build_version = self.get_build_version()

        if not self.build_version:
            sys.exit("Failed to get build version.")

        self.protos_path = os.path.join(self.current_dir, "states", self.build_version, "protos")

        if not os.path.isdir(self.protos_path):
            sys.exit("Please update protos using extract script.")
        
        self.proto_modules = {}
        self.import_protos()
        self.pc = self.proto_modules["_PacketCommand_pb2"].PacketCommand

        self.packet_buffer = b''
        self.capture_info = {}

    def get_build_version(self):
        build_version_file = os.path.join(self.current_dir, "BuildVersion.txt")

        with open(build_version_file, "r", encoding="utf-8") as f:
            return f.read().strip()

    def import_protos(self):
        # Add folder to sys.path so submodules can import correctly
        sys.path.insert(0, self.protos_path)

        for root, dirs, files in os.walk(self.protos_path):
            for file in files:
                if file.endswith("_pb2.py"):
                    full_path = os.path.join(root, file)
                    
                    rel_path = os.path.relpath(full_path, self.protos_path)
                    module_name = rel_path.replace(os.sep, ".").replace(".py", "")
                    
                    # Import dynamically
                    spec = importlib.util.spec_from_file_location(module_name, full_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    self.proto_modules[module_name] = module
        
                    # Bring its public names into globals()
                    for attr in dir(module):
                        if not attr.startswith("_"):
                            globals()[attr] = getattr(module, attr)
                            
    def capture(self):
        capture = pyshark.LiveCapture(
            interface=self.interface,
            bpf_filter='tcp portrange 20200-20300'
        )

        print("Starting continuous capture... Press Ctrl+C to stop.")

        try:
            for packet in capture.sniff_continuously():
                try:
                    if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload'):

                        # Append new TCP payload
                        self.packet_buffer += packet.tcp.payload.binary_value

                        # Process as many packets as possible
                        while True:

                            # Need at least header
                            if len(self.packet_buffer) < 8:
                                break

                            packet_length, proto_type, random_padding = struct.unpack(
                                "<IHH", self.packet_buffer[:8]
                            )

                            # Sanity checks
                            if proto_type not in self.pc.values():
                                print("Invalid proto type, clearing buffer")
                                self.packet_buffer = b''
                                break

                            if packet_length > 9154122 or packet_length < 8:
                                print("Invalid packet length, clearing buffer")
                                self.packet_buffer = b''
                                break

                            # Wait for full packet
                            if len(self.packet_buffer) < packet_length:
                                #print(f"{len(self.packet_buffer)} < {packet_length}")
                                break

                            name = self.pc.Name(proto_type)
                            
                            # Debug statments
                            #print(name, packet_length, proto_type, random_padding)
                            #print(f"{len(self.packet_buffer)} >= {packet_length}")

                            # Extract full packet
                            packet = self.packet_buffer[:packet_length]

                            # Remove packet from buffer
                            self.packet_buffer = self.packet_buffer[packet_length:]

                            # Extract protobuf payload
                            packet_data = packet[8:]

                            # Parse
                            self.parse_proto(packet_data, name)

                except AttributeError:
                    continue

        except KeyboardInterrupt:
            print("\nStopping capture...")
        finally:
            capture.close()

    def parse_proto(self, packet_data, name):
        message_class = globals().get("S" + name)
        if not message_class:
            print(f"No proto class named {name}")

        try:
            message = message_class()
            message.ParseFromString(packet_data)
            handler = self.capture_info.get(name)
            if handler:
                print(f"{name} -> {handler.__name__}")
                handler(self, message, name)
        except Exception as e:
            print(f"Error parsing proto {name}: {e}")
            with open("dump.bin", "wb") as f:
                f.write(packet_data)
            exit()

if __name__ == "__main__":
    dc = DarkandDarkerCapture("Ethernet")
    dc.capture()