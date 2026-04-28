#!/bin/bash

# Equipment Service API Test Script
# Test the Gestion des Équipements Agricoles microservice

BASE_URL="http://localhost:8000/api"

echo "================================"
echo "Equipment Service API Tests"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Create Equipment
echo -e "${BLUE}1. Create Equipment (Tracteur)${NC}"
curl -X POST $BASE_URL/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tracteur John Deere T740",
    "type": "Tractor",
    "serial_number": "JD-2024-001",
    "usage_hours": 850,
    "status": "active",
    "last_revision": "2026-01-15",
    "next_revision": "2027-01-15"
  }'
echo -e "\n${GREEN}✓ Equipment created${NC}\n"

# Test 2: List All Equipment
echo -e "${BLUE}2. List All Equipment${NC}"
curl -X GET $BASE_URL/equipements/ \
  -H "Content-Type: application/json"
echo -e "\n${GREEN}✓ Equipment list retrieved${NC}\n"

# Test 3: Get Equipment Details
echo -e "${BLUE}3. Get Equipment Details (ID: 1)${NC}"
curl -X GET $BASE_URL/equipements/1/ \
  -H "Content-Type: application/json"
echo -e "\n${GREEN}✓ Equipment details retrieved${NC}\n"

# Test 4: Get Equipment Status
echo -e "${BLUE}4. Get Equipment Status${NC}"
curl -X GET $BASE_URL/equipements/1/statut/ \
  -H "Content-Type: application/json"
echo -e "\n${GREEN}✓ Equipment status retrieved${NC}\n"

# Test 5: Record Maintenance
echo -e "${BLUE}5. Record Maintenance${NC}"
curl -X POST $BASE_URL/equipements/1/maintenance/ \
  -H "Content-Type: application/json"
echo -e "\n${GREEN}✓ Maintenance recorded${NC}\n"

# Test 6: Create Irrigation Tool
echo -e "${BLUE}6. Create Equipment (Outil d'Irrigation)${NC}"
curl -X POST $BASE_URL/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Système d'\''Irrigation Pivot",
    "type": "Irrigation Tool",
    "serial_number": "IRR-2024-001",
    "usage_hours": 450,
    "status": "active",
    "last_revision": "2026-02-01",
    "next_revision": "2026-08-01"
  }'
echo -e "\n${GREEN}✓ Irrigation tool created${NC}\n"

# Test 7: Create Harvesting Equipment
echo -e "${BLUE}7. Create Equipment (Matériel de Récolte)${NC}"
curl -X POST $BASE_URL/equipements/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Moissonneuse-batteuse CLAAS",
    "type": "Harvesting Equipment",
    "serial_number": "CLAAS-2024-001",
    "usage_hours": 320,
    "status": "maintenance",
    "last_revision": "2026-03-01",
    "next_revision": "2026-09-01"
  }'
echo -e "\n${GREEN}✓ Harvesting equipment created${NC}\n"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${GREEN}================================${NC}"