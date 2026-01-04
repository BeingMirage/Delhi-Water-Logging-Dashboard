import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import WardDetail from './components/WardDetail';

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <div className="navbar">
          <div className="navbar-content">
            <div className="brand">
              <div className="brand-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/1200px-Emblem_of_India.svg.png" alt="Emblem" style={{ width: '24px', height: 'auto' }} />
              </div>
              <div className="brand-text">
                <h1>Urban Water-Logging Dashboard</h1>
                <p>Built for HACK4DELHI</p>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
              <nav style={{ display: 'flex', gap: '1.5rem', fontSize: '0.95rem', fontWeight: '500' }}>
                <Link to="/" style={{ textDecoration: 'none', color: 'var(--primary-color)' }}>Dashboard</Link>
                <span style={{ color: '#999', cursor: 'not-allowed' }}>Reports</span>
                <span style={{ color: '#999', cursor: 'not-allowed' }}>Alerts</span>
              </nav>
              <div style={{ fontSize: '0.9rem', color: '#666', borderLeft: '1px solid #eee', paddingLeft: '1.5rem' }}>
                {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </div>
            </div>
          </div>
        </div>
        
        <div className="container" style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ward/:id" element={<WardDetail />} />
          </Routes>
        </div>

        <footer style={{ background: 'white', borderTop: '1px solid #eee', padding: '1.5rem 0', marginTop: '3rem' }}>
          <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: '#666' }}>
            <div>
              &copy; 2026 Department of Urban Development, GNCTD. All rights reserved.
            </div>
            <div style={{ display: 'flex', gap: '1.5rem' }}>
              <span>Privacy Policy</span>
              <span>Terms of Service</span>
              <span>Contact Support</span>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
