REM Change paths as needed
protodump -file "C:\Program Files\IRONMACE\Dark and Darker\DungeonCrawler\Binaries\Win64\DungeonCrawler.exe" -output protos
pip install protobuf
pip install --upgrade protobuf
protoc --proto_path=protos --python_out=protos protos/*.protoc 
pause