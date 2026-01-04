import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useNavigate } from 'react-router-dom';

const MapRisk = ({ data }) => {
  const navigate = useNavigate();
  const position = [28.6139, 77.2090]; // Delhi coordinates

  const getColor = (risk) => {
    switch (risk) {
      case 'High': return '#d32f2f'; // Matches var(--risk-high)
      case 'Medium': return '#fbc02d'; // Matches var(--risk-medium)
      case 'Low': return '#1976d2'; // Matches var(--risk-low)
      default: return '#666';
    }
  };

  return (
    <MapContainer center={position} zoom={11} style={{ height: '100%', width: '100%', borderRadius: '8px', zIndex: 0 }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {data.map((ward) => (
        <CircleMarker
          key={ward.ward_id}
          center={[ward.latitude, ward.longitude]}
          pathOptions={{ color: getColor(ward.risk_level), fillColor: getColor(ward.risk_level), fillOpacity: 0.7 }}
          radius={10}
          eventHandlers={{
            click: () => navigate(`/ward/${ward.ward_id}`),
          }}
        >
          <Popup>
            <div style={{ textAlign: 'center', minWidth: '150px' }}>
              <strong style={{ fontSize: '1.1em', display: 'block', marginBottom: '0.25rem' }}>{ward.ward_name}</strong>
              <div style={{ fontSize: '0.85em', color: '#666', marginBottom: '0.5rem' }}>{ward.locality}</div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #eee', paddingTop: '0.5rem' }}>
                <span style={{ color: getColor(ward.risk_level), fontWeight: 'bold' }}>{ward.risk_level} Risk</span>
                <span style={{ background: '#eee', padding: '2px 6px', borderRadius: '4px', fontSize: '0.8em' }}>Score: {ward.preparedness_score}</span>
              </div>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default MapRisk;
