import pandas as pd
import os

DATA_DIR = 'backend/data'
RAINFALL_FILE = os.path.join(DATA_DIR, 'rainfall_weather_mock_data.csv')
DRAINAGE_FILE = os.path.join(DATA_DIR, 'drainage_infrastructure_mock_data.csv')
CENTROID_FILE = os.path.join(DATA_DIR, 'delhi_ward_centroids.csv')

try:
    rainfall_df = pd.read_csv(RAINFALL_FILE)
    drainage_df = pd.read_csv(DRAINAGE_FILE)
    centroid_df = pd.read_csv(CENTROID_FILE)
    
    print("--- Data Loaded ---")
    print("Rainfall Columns:", rainfall_df.columns.tolist())
    print("Drainage Columns:", drainage_df.columns.tolist())
    print("Centroid Columns:", centroid_df.columns.tolist())
    
    print("\n--- Ward IDs Sample ---")
    print("Rainfall Ward IDs:", rainfall_df['ward_id'].unique()[:5])
    print("Drainage Ward IDs:", drainage_df['ward_id'].unique()[:5])
    print("Centroid Ward IDs:", centroid_df['ward_id'].unique()[:5])
    
    # Check for whitespace
    print("\n--- Whitespace Check ---")
    print("Drainage Ward ID 'Ward_1' length:", len(drainage_df['ward_id'].iloc[0]))
    print("Value:", repr(drainage_df['ward_id'].iloc[0]))
    
    # Simulate Logic
    print("\n--- Simulation ---")
    rainfall_summary = rainfall_df.groupby('ward_id')['rainfall_intensity_mm_per_hr'].mean().reset_index()
    print("Rainfall Summary Sample:\n", rainfall_summary.head())
    
    merged = pd.merge(rainfall_summary, drainage_df, on='ward_id', how='left')
    print("\nMerged Sample:\n", merged[['ward_id', 'rainfall_intensity_mm_per_hr', 'drain_capacity_mm_per_hr']].head())
    
    def calculate_risk(rainfall_intensity, drain_capacity):
        if drain_capacity == 0:
            return "High"
        ratio = rainfall_intensity / drain_capacity
        if ratio > 1.0:
            return "High"
        elif ratio > 0.8:
            return "Medium"
        else:
            return "Low"

    print("\n--- Risk Calculation ---")
    for _, row in merged.head().iterrows():
        r = row['rainfall_intensity_mm_per_hr']
        d = row['drain_capacity_mm_per_hr']
        risk = calculate_risk(r, d)
        print(f"Ward: {row['ward_id']}, Rain: {r}, Cap: {d}, Risk: {risk}")

except Exception as e:
    print(f"Error: {e}")
