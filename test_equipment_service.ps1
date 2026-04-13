# Equipment Service API Test Script (PowerShell)
# Test the Gestion des Équipements Agricoles microservice

$BASE_URL = "http://localhost:8000/api"

Write-Host "================================" -ForegroundColor Green
Write-Host "Equipment Service API Tests" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Test 1: Create Equipment (Tracteur)
Write-Host "1. Create Equipment (Tracteur)" -ForegroundColor Blue

$body = @{
    name = "Tracteur John Deere T740"
    type = "Tractor"
    serial_number = "JD-2024-001"
    usage_hours = 850
    status = "active"
    last_revision = "2026-01-15"
    next_revision = "2027-01-15"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Equipment created" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: List All Equipment
Write-Host "2. List All Equipment" -ForegroundColor Blue

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/" `
        -Method GET `
        -ContentType "application/json"
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Equipment list retrieved" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Get Equipment Details (ID: 1)
Write-Host "3. Get Equipment Details (ID: 1)" -ForegroundColor Blue

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/1/" `
        -Method GET `
        -ContentType "application/json"
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Equipment details retrieved" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Get Equipment Status
Write-Host "4. Get Equipment Status" -ForegroundColor Blue

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/1/statut/" `
        -Method GET `
        -ContentType "application/json"
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Equipment status retrieved" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 5: Record Maintenance
Write-Host "5. Record Maintenance" -ForegroundColor Blue

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/1/maintenance/" `
        -Method POST `
        -ContentType "application/json"
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Maintenance recorded" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 6: Create Irrigation Tool
Write-Host "6. Create Equipment (Outil d'Irrigation)" -ForegroundColor Blue

$body = @{
    name = "Système d'Irrigation Pivot"
    type = "Irrigation Tool"
    serial_number = "IRR-2024-001"
    usage_hours = 450
    status = "active"
    last_revision = "2026-02-01"
    next_revision = "2026-08-01"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Irrigation tool created" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 7: Create Harvesting Equipment
Write-Host "7. Create Equipment (Matériel de Récolte)" -ForegroundColor Blue

$body = @{
    name = "Moissonneuse-batteuse CLAAS"
    type = "Harvesting Equipment"
    serial_number = "CLAAS-2024-001"
    usage_hours = 320
    status = "maintenance"
    last_revision = "2026-03-01"
    next_revision = "2026-09-01"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/equipements/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
    Write-Host "✓ Harvesting equipment created" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "================================" -ForegroundColor Green
Write-Host "All tests completed!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green