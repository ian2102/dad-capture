# Dark and Darker Network Capture

A tool to capture dark and darker network trafic.

## Prerequisites

1. **Python**: Download from: [Python's official website](https://www.python.org/downloads/).

2. **Wireshark (includes TShark)**: Download from: [Wireshark's official website](https://www.wireshark.org/download.html).

3. **Protocol Buffers**: Download from: [Protobuf's official website](https://protobuf.dev/installation/).

   ```cmd
   winget install protobuf
   ```

4. **Python dependencies (PyShark + Protobuf Python package)**

   ```cmd
   pip install pyshark protobuf
   ```

## Usage

1. **Extract and Compile Proto Files (required after every game update)**

   You must configure the path to the game executable inside extract.ps1:
   
   ```powershell
   $DungeonCrawlerExe = "C:\Program Files\IRONMACE\Dark and Darker\DungeonCrawler\Binaries\Win64\DungeonCrawler.exe"
   ```

   Then run:
   
   ```cmd
   extract.ps1
   ```

1. **Configure the network interface**

   Open `main.py` and set your network adapter:
   ```python
   INTERFACE = "Ethernet"
   ```

2. **Run the capture script**

   ```cmd
   python main.py
   ```

3. **Output location**

   Captured data is saved automatically to:
   ```
   data/<command_name>/<timestamp>.txt
   ```

4. **Stop the program**

   Press `CTRL + C` in the terminal to stop packet capture.


## Disclaimer

This project is not affiliated with or endorsed by Ironmace or Dark and Darker. Use responsibly and in accordance with the game's terms of service.


