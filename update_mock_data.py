import pandas as pd
import numpy as np
import os

DATA_DIR = 'backend/data'
RAINFALL_FILE = os.path.join(DATA_DIR, 'rainfall_weather_mock_data.csv')
DRAINAGE_FILE = os.path.join(DATA_DIR, 'drainage_infrastructure_mock_data.csv')

# Load
rainfall_df = pd.read_csv(RAINFALL_FILE)
drainage_df = pd.read_csv(DRAINAGE_FILE)

# Clean IDs
rainfall_df['ward_id'] = rainfall_df['ward_id'].astype(str).str.strip()
drainage_df['ward_id'] = drainage_df['ward_id'].astype(str).str.strip()

# Get capacities to know what target to hit
capacities = drainage_df.set_index('ward_id')['drain_capacity_mm_per_hr'].to_dict()

print("Original Max Intensity:", rainfall_df['rainfall_intensity_mm_per_hr'].max())

# Logic to boost rainfall
def boost_rainfall(row):
    ward = row['ward_id']
    cap = capacities.get(ward, 20) # Default 20 if missing
    
    # Make Ward_1, Ward_5, Ward_10 High Risk (Rain > Cap)
    if ward in ['Ward_1', 'Ward_5', 'Ward_10']:
        # Target intensity: 1.2 * Cap to 2.0 * Cap
        return np.random.uniform(1.2 * cap, 2.0 * cap)
    
    # Make Ward_2, Ward_6 Medium Risk (0.8 * Cap < Rain < Cap)
    elif ward in ['Ward_2', 'Ward_6']:
        return np.random.uniform(0.85 * cap, 0.95 * cap)
        
    # Others Low Risk (Rain < 0.5 * Cap)
    else:
        return np.random.uniform(0.1 * cap, 0.5 * cap)

# Apply boost
rainfall_df['rainfall_intensity_mm_per_hr'] = rainfall_df.apply(boost_rainfall, axis=1)
rainfall_df['rainfall_mm'] = rainfall_df['rainfall_intensity_mm_per_hr'] * 24 # Rough approx for daily

print("New Max Intensity:", rainfall_df['rainfall_intensity_mm_per_hr'].max())

# Save back
rainfall_df.to_csv(RAINFALL_FILE, index=False)
print("Updated rainfall_weather_mock_data.csv")
