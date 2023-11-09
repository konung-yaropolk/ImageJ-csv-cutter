#!/usr/bin/powershell -Command

Start-Process -FilePath "python" -ArgumentList "ImageJ-csv-cutter.py " -NoNewWindow -Wait
Write-Host "Press any key to exit..."
Read-Host