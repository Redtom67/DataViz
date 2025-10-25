# Road Safety Dashboard - France 2024

A comprehensive Streamlit dashboard analyzing road accident data in France for 2024.

## Features

- **Global Overview**: Interactive visualizations of accident trends, severity statistics, and geographic distribution
- **Victim Analysis**: Demographics and characteristics of accident victims including age, gender, and vehicle types
- **Location & Environmental Factors**: Analysis of atmospheric conditions, road types, and speed limits
- **Conclusions**: Data-driven recommendations for road safety improvements

## Installation

I recommend creating a virtual environnement

```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:

```bash
streamlit run Dashboard.py
```

## Data Source

Dataset from official French road safety database (2024).
- 

df_dataset.csv

 - Preprocessed accident data
- Includes: locations, times, weather conditions, victim characteristics

## Project Structure

```
├── Dashboard.py                    # Home page
├── pages/
│   ├── 1_Global_Overview.py       # Accident statistics & maps
│   ├── 2_Users_Type.py            # Victim demographics
│   ├── 3_Location_Factors.py      # Environmental analysis
│   └── 4_Conclusions.py           # Key findings
├── data/
│   └── df_dataset.csv             # Main dataset
└── images/                         # Visual assets
```

## Key Insights

- Most accidents involve drivers aged 21-30
- 67% of accidents involve male drivers
- Light vehicles (cars) account for majority of incidents
- Most crashes occur in normal weather on dry roads
- Critical speed zones: 50 km/h and 80 km/h

## Author

**Thomas FISCHER** - DataViz Individual Project