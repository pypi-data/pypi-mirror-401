# surf_scrap

Bibliothèque Python pour extraire les données météo surf depuis surf-report.com

## Installation
```bash
pip install -e .
```

## Utilisation
```python
import surf_scrap

# Extraire les données de Lacanau
df = surf_scrap.extract_surf_data(
    'https://www.surf-report.com/meteo-surf/lacanau-s1043.html',
    'data/lacanau.csv'
)

print(df.head())
```

## Exemples d'URLs supportées

- Lacanau: https://www.surf-report.com/meteo-surf/lacanau-s1043.html
- Carcans: https://www.surf-report.com/meteo-surf/carcans-plage-s1013.html
- Moliets: https://www.surf-report.com/meteo-surf/moliets-plage-centrale-s102799.html
```

---


Part_2 contient :
```
surf_scrap_project/
│
├── surf_scrap/
│   ├── __init__.py
│   └── scraper.py
│
├── output/                  
│   ├── lacanau.csv
│   ├── carcans.csv
│   └── moliets.csv
│
├── setup.py
├── requirements.txt
├── README.md
└── test.py
|__ run_surf_scrap.py