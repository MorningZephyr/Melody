# Activate Virtual Environment Script
# Run this in PowerShell to activate the virtual environment

.\venv\Scripts\Activate.ps1

Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host "You can now run the piano demos:" -ForegroundColor Yellow
Write-Host "  python piano_player.py" -ForegroundColor Cyan
Write-Host "  python advanced_sheet_reader.py" -ForegroundColor Cyan
Write-Host "  python midi_processor.py" -ForegroundColor Cyan
Write-Host "  python music_visualizer.py" -ForegroundColor Cyan
Write-Host "  python demo_runner.py  # Run all demos" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deactivate the virtual environment, run: deactivate" -ForegroundColor Yellow
