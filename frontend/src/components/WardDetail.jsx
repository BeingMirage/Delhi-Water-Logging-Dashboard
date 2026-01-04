import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getWardDetail } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const WardDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getWardDetail(id).then(res => {
      setData(res);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>Loading ward details...</div>;
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--risk-high)' }}>Ward not found</div>;

  return (
    <div>
      <button className="back-btn" onClick={() => navigate('/')}>
        <span>&larr;</span> Back to Dashboard
      </button>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ fontSize: '0.9rem', color: '#666', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '0.25rem' }}>{data.locality}</div>
          <h2 style={{ marginBottom: '0.5rem', fontSize: '2rem', color: 'var(--primary-color)' }}>{data.ward_name}</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span className={`badge badge-${data.risk_level.toLowerCase()}`} style={{ fontSize: '1em', padding: '0.5em 1em', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
              {data.risk_level} Risk
            </span>
            <span style={{ color: '#666', fontSize: '0.9rem' }}>ID: {data.ward_id}</span>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'white', padding: '0.75rem 1.5rem', borderRadius: '50px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid #eee' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.4rem', lineHeight: '1', color: '#333' }}>{data.preparedness_score}</div>
            <div style={{ fontSize: '0.7rem', color: '#666', textTransform: 'uppercase', fontWeight: '600', letterSpacing: '0.5px' }}>Score</div>
          </div>
          <div className={`score-circle ${data.preparedness_score > 70 ? 'score-good' : data.preparedness_score > 40 ? 'score-avg' : 'score-bad'}`} 
               style={{ width: '48px', height: '48px', fontSize: '1.1rem', boxShadow: 'none' }}>
            {data.preparedness_score}
          </div>
        </div>
      </div>

      <div className="card" style={{ 
        borderLeft: `6px solid ${data.risk_level === 'High' ? 'var(--risk-high)' : data.risk_level === 'Medium' ? 'var(--risk-medium)' : 'var(--risk-low)'}`,
        marginBottom: '2rem',
        background: data.risk_level === 'High' ? 'var(--risk-high-bg)' : data.risk_level === 'Medium' ? 'var(--risk-medium-bg)' : 'var(--risk-low-bg)',
        boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
      }}>
        <h3 style={{ color: '#333', marginTop: 0 }}>Risk Analysis</h3>
        <p style={{ fontSize: '1.1em', margin: 0, color: '#444', lineHeight: '1.6' }}>{data.risk_explanation}</p>
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))' }}>
        <div className="card">
          <h3 style={{ borderBottom: '2px solid #f0f0f0', paddingBottom: '0.75rem', marginBottom: '1rem' }}>Drainage Infrastructure</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <li style={{ padding: '1rem 0', borderBottom: '1px solid #f5f5f5', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#666' }}>Capacity</span>
              <strong style={{ color: '#333' }}>{data.drainage_info.capacity} mm/hr</strong>
            </li>
            <li style={{ padding: '1rem 0', borderBottom: '1px solid #f5f5f5', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#666' }}>Condition</span>
              <strong style={{ color: '#333' }}>{data.drainage_info.condition}</strong>
            </li>
            <li style={{ padding: '1rem 0', borderBottom: '1px solid #f5f5f5', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#666' }}>Pump Available</span>
              <strong style={{ color: '#333' }}>{data.drainage_info.pump_available}</strong>
            </li>
            <li style={{ padding: '1rem 0', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#666' }}>Infrastructure Age</span>
              <strong style={{ color: '#333' }}>{data.drainage_info.infrastructure_age}</strong>
            </li>
          </ul>
        </div>
        
        <div className="card">
          <h3 style={{ borderBottom: '2px solid #f0f0f0', paddingBottom: '0.75rem', marginBottom: '1rem' }}>Rainfall Trend</h3>
          <div style={{ height: '500px', marginTop: '1rem' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.rainfall_history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="time" tick={{fontSize: 12, fill: '#888'}} stroke="#ddd" />
                <YAxis label={{ value: 'Intensity (mm/hr)', angle: -90, position: 'insideLeft', style: {fill: '#888'} }} tick={{fontSize: 12, fill: '#888'}} stroke="#ddd" />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                <Legend />
                <Line type="monotone" dataKey="intensity" stroke="var(--primary-color)" strokeWidth={3} activeDot={{ r: 6 }} name="Rainfall Intensity" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WardDetail;
