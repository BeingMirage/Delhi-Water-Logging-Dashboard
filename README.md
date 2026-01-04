# Urban Water-Logging Dashboard

**Built for HACK4DELHI Hackathon**
**Team StuffCoders**
Members
  `Amey Ghatol` 
  `Simar Ahluwalia`
  `Shaivy Ahluwalia`

## 🌊 Overview
The **Urban Water-Logging Dashboard** is a comprehensive, data-driven solution designed to predict, visualize, and manage urban flood risks in Delhi. Built specifically for the **HACK4DELHI** hackathon, this tool empowers city administrators and urban planners with real-time insights into ward-level preparedness against heavy rainfall.

By integrating meteorological data with drainage infrastructure metrics, the dashboard calculates a dynamic **Risk Level** and **Preparedness Score** for each ward, visualizing the data on an interactive geospatial map.

## 🚀 Key Features
- **Geospatial Risk Map**: Interactive map of Delhi visualizing High, Medium, and Low risk zones using color-coded indicators.
- **Real-Time Risk Calculation**: Dynamic algorithms comparing **Rainfall Intensity** vs. **Drainage Capacity** to predict water-logging events.
- **Ward-Level Analytics**: Detailed drill-down views for specific wards (e.g., Connaught Place, Dwarka) showing:
  - Infrastructure Age & Condition
  - Pump Availability
  - Historical Rainfall Trends (Interactive Charts)
- **Preparedness Score**: A composite metric (0-100) evaluating the readiness of a ward's infrastructure.
- **Government-Grade UI**: Designed with the **UX4G Design Kit** aesthetic for a professional, accessible, and responsive user experience suitable for control rooms.

## 🛠️ Tech Stack

### Frontend
- **React.js (Vite)**: Fast, modern UI framework.
- **React-Leaflet**: For rendering interactive geospatial maps.
- **Recharts**: For visualizing rainfall trends and data analytics.
- **CSS Modules & Variables**: Custom theming using the UX4G color palette (Deep Blue, Red/Yellow/Blue risk indicators).

### Backend
- **Flask (Python)**: Lightweight REST API for serving data and handling logic.
- **Pandas**: High-performance data manipulation for processing CSV datasets.
- **Flask-CORS**: Handling Cross-Origin Resource Sharing.

### Data
- **Mock Datasets**:
  - `rainfall_weather_mock_data.csv`: Simulated rainfall intensity and forecast.
  - `drainage_infrastructure_mock_data.csv`: Infrastructure capacity, age, and condition.
  - `delhi_ward_centroids.csv`: Geospatial coordinates for mapping.

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm

### 1. Backend Setup
Navigate to the backend directory and install dependencies:
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*The backend server will start at `http://localhost:5000`.*

### 2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the development server:
```bash
cd frontend
npm install
npm run dev
```
*The application will be accessible at `http://localhost:5173`.*

## 🎨 Color Schema & Design
The application follows a strict government-standard color palette:
- **High Risk**: Red (`#d32f2f`)
- **Medium Risk**: Yellow (`#fbc02d`)
- **Low Risk (Safe)**: Blue (`#1976d2`)
- **Primary Brand**: Deep Blue (`#003366`)

## 🤝 Contribution
This project was developed as a prototype for **HACK4DELHI**. Future improvements could include integration with real-time IMD weather APIs and IoT sensors in drainage networks.

---
*Government of NCT of Delhi - Prototype*
