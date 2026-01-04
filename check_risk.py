import pandas as pd
import os

DATA_DIR = 'backend/data'
RAINFALL_FILE = os.path.join(DATA_DIR, 'rainfall_weather_mock_data.csv')
DRAINAGE_FILE = os.path.join(DATA_DIR, 'drainage_infrastructure_mock_data.csv')

try:
    rainfall_df = pd.read_csv(RAINFALL_FILE)
    drainage_df = pd.read_csv(DRAINAGE_FILE)
    
    # Clean
    rainfall_df.columns = rainfall_df.columns.str.strip()
    drainage_df.columns = drainage_df.columns.str.strip()
    rainfall_df['ward_id'] = rainfall_df['ward_id'].astype(str).str.strip()
    drainage_df['ward_id'] = drainage_df['ward_id'].astype(str).str.strip()

    rainfall_summary = rainfall_df.groupby('ward_id')['rainfall_intensity_mm_per_hr'].mean().reset_index()
    merged = pd.merge(rainfall_summary, drainage_df, on='ward_id', how='left')
    
    print("--- Risk Analysis ---")
    for _, row in merged.iterrows():
        r = row['rainfall_intensity_mm_per_hr']
        d = row['drain_capacity_mm_per_hr']
        ratio = r / d if d > 0 else 999
        if ratio > 0.5: # Check even lower threshold
            print(f"Ward: {row['ward_id']}, Rain: {r:.2f}, Cap: {d}, Ratio: {ratio:.2f}")
            
    print("Max Ratio:", (merged['rainfall_intensity_mm_per_hr'] / merged['drain_capacity_mm_per_hr']).max())

except Exception as e:
    print(e)
