MOCK_LANDS = {
    1: {"id": 1, "name": "Parcelle Nord", "surface": 5.2, "soil_type": "argileux", "crop_planted": "blé"},
    2: {"id": 2, "name": "Parcelle Sud",  "surface": 3.8, "soil_type": "sableux",  "crop_planted": "tomates"},
    3: {"id": 3, "name": "Parcelle Est",  "surface": 7.0, "soil_type": "limoneux", "crop_planted": "pommes de terre"},
}

MOCK_CULTURES = {
    1: {"id": 1, "name": "Blé",             "plantation_date": "2024-01-15", "harvest_date": "2024-06-01"},
    2: {"id": 2, "name": "Tomates",         "plantation_date": "2024-03-01", "harvest_date": "2024-07-15"},
    3: {"id": 3, "name": "Pommes de terre", "plantation_date": "2024-02-10", "harvest_date": "2024-08-01"},
}

MOCK_EQUIPMENTS = {
    1: {"id": 1, "name": "Tracteur John Deere", "type": "tracteur",  "status": "available"},
    2: {"id": 2, "name": "Système Irrigation",  "type": "irrigation","status": "in_use"},
    3: {"id": 3, "name": "Moissonneuse",        "type": "harvest",   "status": "maintenance"},
}
