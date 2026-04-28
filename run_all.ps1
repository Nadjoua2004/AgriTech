# AgriTech Local Run Script (PowerShell)
# This script starts all microservices and the frontend.

$Services = @(
    @{ Name = "Auth Service"; Path = "services/auth_service"; Port = 8001; Command = "python manage.py runserver 8001" },
    @{ Name = "Equipment Service"; Path = "services/equipment_service"; Port = 8003; Command = "python manage.py runserver 8003" },
    @{ Name = "Terre Service"; Path = "services/terre_service"; Port = 8004; Command = "python manage.py runserver 8004" },
    @{ Name = "Worker Service"; Path = "services/worker_service"; Port = 8005; Command = "python manage.py runserver 8005" },
    @{ Name = "Cultures Service"; Path = "services/cultures_service"; Port = 8002; Command = "python main.py" }, # FastAPI
    @{ Name = "Frontend"; Path = "frontend"; Port = 8000; Command = "python manage.py runserver 8000" }
)

Write-Host "Starting AgriTech Platform..." -ForegroundColor Cyan

foreach ($Service in $Services) {
    Write-Host "Launching $($Service.Name) on port $($Service.Port)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $($Service.Path); $($Service.Command)"
}

Write-Host "All services launched in separate windows." -ForegroundColor Green
Write-Host "Frontend should be available at http://localhost:8000" -ForegroundColor Green
