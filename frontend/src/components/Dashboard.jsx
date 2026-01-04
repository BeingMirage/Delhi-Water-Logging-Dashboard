import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWards, getMapData } from '../api';
import MapRisk from './MapRisk';

const Dashboard = () => {
  const [wards, setWards] = useState([]);
  const [mapData, setMapData] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([getWards(), getMapData()])
      .then(([wardsData, mapDataRes]) => {
        setWards(wardsData);
        setMapData(mapDataRes);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>Loading dashboard data...</div>;

  const getCardColor = (risk) => {
    switch (risk) {
      case 'High': return 'var(--risk-high-bg)';
      case 'Medium': return 'var(--risk-medium-bg)';
      case 'Low': return 'var(--risk-low-bg)';
      default: return 'white';
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Ward Overview</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--risk-high)' }}></span> High Risk
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#fbc02d' }}></span> Medium Risk
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem' }}>
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--risk-low)' }}></span> Low Risk
          </div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '2rem', padding: '0', overflow: 'hidden', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}>
        <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid #eee', background: '#fff' }}>
          <h3 style={{ margin: 0, fontSize: '1.1rem', color: '#444' }}>Geospatial Risk Map</h3>
        </div>
        <div style={{ height: '600px' }}>
          <MapRisk data={mapData} />
        </div>
      </div>

      <div className="grid">
        {wards.map(ward => (
          <div 
            key={ward.ward_id} 
            className="card" 
            onClick={() => navigate(`/ward/${ward.ward_id}`)}
            style={{ 
              backgroundColor: getCardColor(ward.risk_level),
              border: '1px solid rgba(0,0,0,0.05)',
              cursor: 'pointer'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div>
                <h3 style={{ margin: 0, fontSize: '1.2rem', color: '#333' }}>{ward.ward_name}</h3>
                <div style={{ fontSize: '0.85rem', color: '#666', marginTop: '0.25rem' }}>{ward.locality}</div>
              </div>
              <span className={`badge badge-${ward.risk_level.toLowerCase()}`} style={{ backgroundColor: 'rgba(255,255,255,0.8)', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                {ward.risk_level} Risk
              </span>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto' }}>
              <div style={{ fontSize: '0.9rem' }}>
                <div style={{ marginBottom: '0.5rem', color: '#555' }}>
                  <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', color: '#777', fontWeight: '600' }}>Rainfall</span>
                  {ward.average_rainfall_intensity} mm/hr
                </div>
                <div style={{ color: '#555' }}>
                  <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', color: '#777', fontWeight: '600' }}>Drain Cap</span>
                  {ward.drain_capacity} mm/hr
                </div>
              </div>
              
              <div style={{ textAlign: 'center' }}>
                <div className={`score-circle ${ward.preparedness_score > 70 ? 'score-good' : ward.preparedness_score > 40 ? 'score-avg' : 'score-bad'}`}
                     style={{ width: '56px', height: '56px', fontSize: '1.2rem', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
                  {ward.preparedness_score}
                </div>
                <div style={{ fontSize: '0.7rem', marginTop: '0.5rem', fontWeight: '600', color: '#666', textTransform: 'uppercase' }}>Score</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
