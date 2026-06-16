# Download BuildVersion.txt
$Url = "http://cdn.darkanddarker.com/Dark%20and%20Darker/Build/BuildVersion.txt"
$OutputFile = "BuildVersion.txt"

Write-Host "Downloading version from $Url ..."

try {
    Invoke-WebRequest -Uri $Url -OutFile $OutputFile -ErrorAction Stop
    Write-Host "Download complete. Saved as $OutputFile"
} catch {
    Write-Host "Failed to download file. Error: $_"
    exit 1
}

# Read build version
try {
    $BuildVersion = Get-Content $OutputFile -Raw
    $BuildVersion = $BuildVersion.Trim()  # Remove any whitespace/newlines
    Write-Host "Detected Build Version: $BuildVersion"
} catch {
    Write-Host "Failed to read BuildVersion.txt. Error: $_"
    exit 1
}

# Prepare output folder
$ProtoOutput = Join-Path -Path "states" -ChildPath (Join-Path -Path $BuildVersion -ChildPath "protos")

if (-Not (Test-Path $ProtoOutput)) {
    New-Item -ItemType Directory -Path $ProtoOutput | Out-Null
}

# Run Protodump
$DungeonCrawlerExe = "C:\Program Files\IRONMACE\Dark and Darker\DungeonCrawler\Binaries\Win64\DungeonCrawler.exe"

Write-Host "Running protodump..."
try {
    & protodump -file $DungeonCrawlerExe -output $ProtoOutput
    Write-Host "Protodump complete. Output: $ProtoOutput"
} catch {
    Write-Host "Protodump failed. Make sure protodump is in your PATH. Error: $_"
    exit 1
}

# Compile .protoc files to Python
Write-Host "Compiling .protoc files..."
try {
    & protoc --proto_path=$ProtoOutput --python_out=$ProtoOutput "$ProtoOutput/*.proto"
    Write-Host "Compilation complete."
} catch {
    Write-Host "Protoc compilation failed. Make sure protoc is installed and in your PATH."
    exit 1
}

Write-Host "All tasks completed successfully."
pause