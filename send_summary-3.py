<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stuart.parking.summary</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/stuartbanham/Parking/send_summary.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>20</integer>
        <key>Minute</key><integer>5</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/stuartbanham/Parking/logs/summary.out</string>

    <key>StandardErrorPath</key>
    <string>/Users/stuartbanham/Parking/logs/summary.err</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
