from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load Data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RAINFALL_FILE = os.path.join(DATA_DIR, 'rainfall_weather_mock_data.csv')
DRAINAGE_FILE = os.path.join(DATA_DIR, 'drainage_infrastructure_mock_data.csv')
CENTROID_FILE = os.path.join(DATA_DIR, 'delhi_ward_centroids.csv')

try:
    rainfall_df = pd.read_csv(RAINFALL_FILE)
    drainage_df = pd.read_csv(DRAINAGE_FILE)
    centroid_df = pd.read_csv(CENTROID_FILE)
    
    # Clean Data
    # 1. Strip whitespace from column names
    rainfall_df.columns = rainfall_df.columns.str.strip()
    drainage_df.columns = drainage_df.columns.str.strip()
    centroid_df.columns = centroid_df.columns.str.strip()
    
    # 2. Ensure ward_id is string and stripped of whitespace
    rainfall_df['ward_id'] = rainfall_df['ward_id'].astype(str).str.strip()
    drainage_df['ward_id'] = drainage_df['ward_id'].astype(str).str.strip()
    centroid_df['ward_id'] = centroid_df['ward_id'].astype(str).str.strip()

    print("Data loaded and cleaned successfully.")
    print(f"Loaded {len(drainage_df)} drainage records.")
    print(f"Sample Ward IDs: {drainage_df['ward_id'].head().tolist()}")
except Exception as e:
    print(f"Error loading data: {e}")
    rainfall_df = pd.DataFrame()
    drainage_df = pd.DataFrame()
    centroid_df = pd.DataFrame()

# Mock Ward Names and Localities
WARD_INFO = {
    "Ward_1": {"name": "Connaught Place", "locality": "Central Delhi"},
    "Ward_2": {"name": "Karol Bagh", "locality": "Central Delhi"},
    "Ward_3": {"name": "Chandni Chowk", "locality": "Old Delhi"},
    "Ward_4": {"name": "Dwarka", "locality": "South West Delhi"},
    "Ward_5": {"name": "Rohini", "locality": "North West Delhi"},
    "Ward_6": {"name": "Lajpat Nagar", "locality": "South Delhi"},
    "Ward_7": {"name": "Hauz Khas", "locality": "South Delhi"},
    "Ward_8": {"name": "Vasant Kunj", "locality": "South West Delhi"},
    "Ward_9": {"name": "Pitampura", "locality": "North West Delhi"},
    "Ward_10": {"name": "Janakpuri", "locality": "West Delhi"},
    "Ward_11": {"name": "Mayur Vihar", "locality": "East Delhi"},
    "Ward_12": {"name": "Saket", "locality": "South Delhi"},
    "Ward_13": {"name": "Greater Kailash", "locality": "South Delhi"},
    "Ward_14": {"name": "Punjabi Bagh", "locality": "West Delhi"},
    "Ward_15": {"name": "Model Town", "locality": "North Delhi"},
    "Ward_16": {"name": "Okhla", "locality": "South East Delhi"},
    "Ward_17": {"name": "Nehru Place", "locality": "South East Delhi"},
    "Ward_18": {"name": "Shahdara", "locality": "North East Delhi"},
    "Ward_19": {"name": "Laxmi Nagar", "locality": "East Delhi"},
    "Ward_20": {"name": "Patel Nagar", "locality": "Central Delhi"}
}

def calculate_risk(rainfall_intensity, drain_capacity):
    # Handle missing or zero capacity
    if pd.isna(drain_capacity) or drain_capacity <= 0:
        # If we have rainfall but no drain info, it's technically high risk or unknown.
        # But for MVP, if data is missing, let's default to High to alert user, 
        # OR check if rainfall is 0.
        if rainfall_intensity == 0:
            return "Low"
        return "High"
    
    ratio = rainfall_intensity / drain_capacity
    if ratio > 1.0:
        return "High"
    elif ratio > 0.8:
        return "Medium"
    else:
        return "Low"

def calculate_preparedness_score(row):
    score = 0
    
    # 1. Drain Condition (Max 30)
    condition = str(row.get('drain_condition', '')).lower()
    if condition == 'good':
        score += 30
    elif condition == 'fair':
        score += 15
    
    # 2. Pump Availability (Max 20)
    pump = str(row.get('pump_available', '')).lower()
    if pump == 'yes' or pump == 'true':
        score += 20
        
    # 3. Infrastructure Age (Max 20)
    # Assuming format is like "0-5 years", "10-20 years" or just a string category
    # For MVP, let's do simple string matching or default to mid-tier if unknown
    age = str(row.get('infrastructure_age_category', '')).lower()
    if 'new' in age or '0-5' in age or '5-10' in age:
        score += 20
    elif 'moderate' in age or '10-20' in age:
        score += 10
    
    # 4. Drain Capacity (Max 30)
    capacity = row.get('drain_capacity_mm_per_hr', 0)
    if capacity >= 50:
        score += 30
    elif capacity >= 20:
        score += 15
    else:
        score += 5
        
    return min(score, 100)

@app.route('/wards', methods=['GET'])
def get_wards():
    # Aggregate rainfall data by ward (mean intensity)
    rainfall_summary = rainfall_df.groupby('ward_id')['rainfall_intensity_mm_per_hr'].mean().reset_index()
    
    # Merge with drainage data
    merged = pd.merge(rainfall_summary, drainage_df, on='ward_id', how='left')
    
    wards_list = []
    for _, row in merged.iterrows():
        avg_rainfall = row['rainfall_intensity_mm_per_hr']
        drain_capacity = row['drain_capacity_mm_per_hr']
        
        risk = calculate_risk(avg_rainfall, drain_capacity)
        score = calculate_preparedness_score(row)
        
        ward_id = row['ward_id']
        info = WARD_INFO.get(ward_id, {"name": f"Ward {ward_id}", "locality": "Delhi"})

        wards_list.append({
            "ward_id": ward_id,
            "ward_name": info["name"],
            "locality": info["locality"],
            "average_rainfall_intensity": float(round(avg_rainfall, 2)),
            "drain_capacity": float(drain_capacity) if pd.notna(drain_capacity) else 0.0,
            "risk_level": risk,
            "preparedness_score": int(score)
        })
        
    return jsonify(wards_list)

@app.route('/ward/<ward_id>', methods=['GET'])
def get_ward_detail(ward_id):
    # Clean input ward_id
    ward_id = str(ward_id).strip()
    print(f"Fetching details for ward_id: '{ward_id}'")

    # Check if ward_id is in the dataframe
    # We check both rainfall and drainage to be safe, but prioritize drainage for details
    has_drainage = ward_id in drainage_df['ward_id'].values
    has_rainfall = ward_id in rainfall_df['ward_id'].values
    
    if not has_drainage and not has_rainfall:
        print(f"Ward '{ward_id}' not found in any dataset.")
        return jsonify({"error": "Ward not found"}), 404

    # Get Drainage Info (handle missing)
    if has_drainage:
        ward_drainage = drainage_df[drainage_df['ward_id'] == ward_id].iloc[0]
        drain_capacity = float(ward_drainage['drain_capacity_mm_per_hr'])
        drain_condition = str(ward_drainage['drain_condition'])
        pump_available = str(ward_drainage['pump_available'])
        infrastructure_age = str(ward_drainage['infrastructure_age_category'])
    else:
        # Default values if drainage info is missing
        ward_drainage = {}
        drain_capacity = 0.0
        drain_condition = "Unknown"
        pump_available = "Unknown"
        infrastructure_age = "Unknown"

    # Get Rainfall Info
    ward_rainfall = rainfall_df[rainfall_df['ward_id'].astype(str) == str(ward_id)]
    
    # Prepare time series data
    # Assuming 'date' column exists. Sort by date.
    if not ward_rainfall.empty and 'date' in ward_rainfall.columns:
        ward_rainfall = ward_rainfall.sort_values(by='date')
    
    rainfall_series = []
    for _, row in ward_rainfall.iterrows():
        rainfall_series.append({
            "time": str(row['date']),
            "intensity": float(row['rainfall_intensity_mm_per_hr']),
            "amount_mm": float(row['rainfall_mm'])
        })
        
    # Calculate current/latest risk and score
    avg_rainfall = float(ward_rainfall['rainfall_intensity_mm_per_hr'].mean()) if not ward_rainfall.empty else 0.0
    
    risk = calculate_risk(avg_rainfall, drain_capacity)
    # For score, we need a row-like object. If ward_drainage is empty, we need to construct one or handle it.
    if has_drainage:
        score = int(calculate_preparedness_score(ward_drainage))
    else:
        score = 0 # Or some default
    
    info = WARD_INFO.get(ward_id, {"name": f"Ward {ward_id}", "locality": "Delhi"})

    # Risk Explanation
    explanation = ""
    if risk == "High":
        explanation = f"Rainfall intensity ({round(avg_rainfall, 2)} mm/hr) exceeds drain capacity ({drain_capacity} mm/hr)."
    elif risk == "Medium":
        explanation = f"Rainfall intensity ({round(avg_rainfall, 2)} mm/hr) is nearing drain capacity ({drain_capacity} mm/hr)."
    else:
        explanation = f"Drain capacity ({drain_capacity} mm/hr) is sufficient for current rainfall ({round(avg_rainfall, 2)} mm/hr)."

    response = {
        "ward_id": ward_id,
        "ward_name": info["name"],
        "locality": info["locality"],
        "drainage_info": {
            "capacity": drain_capacity,
            "condition": drain_condition,
            "pump_available": pump_available,
            "infrastructure_age": infrastructure_age
        },
        "rainfall_history": rainfall_series,
        "risk_level": risk,
        "risk_explanation": explanation,
        "preparedness_score": score
    }
    
    return jsonify(response)

@app.route('/map-data', methods=['GET'])
def get_map_data():
    # Aggregate rainfall data by ward (mean intensity)
    rainfall_summary = rainfall_df.groupby('ward_id')['rainfall_intensity_mm_per_hr'].mean().reset_index()
    
    # Merge with drainage data
    merged = pd.merge(rainfall_summary, drainage_df, on='ward_id', how='left')
    
    # Merge with centroid data
    if not centroid_df.empty:
        final_merged = pd.merge(merged, centroid_df, on='ward_id', how='inner')
        
        map_data = []
        for _, row in final_merged.iterrows():
            avg_rainfall = row['rainfall_intensity_mm_per_hr']
            drain_capacity = row.get('drain_capacity_mm_per_hr', 0)
            
            risk = calculate_risk(avg_rainfall, drain_capacity)
            score = calculate_preparedness_score(row)
            
            ward_id = row['ward_id']
            info = WARD_INFO.get(ward_id, {"name": f"Ward {ward_id}", "locality": "Delhi"})

            map_data.append({
                "ward_id": ward_id,
                "ward_name": info["name"],
                "locality": info["locality"],
                "latitude": float(row['latitude']),
                "longitude": float(row['longitude']),
                "risk_level": risk,
                "preparedness_score": int(score)
            })
            
        return jsonify(map_data)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
