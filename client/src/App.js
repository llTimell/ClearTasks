import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './componenets/Login';
import Register from './componenets/Register';
import './App.css';

function App() {
  return (
    <Router>
      <div style={{ textAlign: 'center', margin: '20px' }}>
        <h1>ClearTasks Cloud Project</h1>
        {/* Navigation Buttons */}
        <div className="nav-buttons">
          <Link to="/login" className="link-button">
            Login
          </Link>
          <Link to="/register" className="link-button">
            Register
          </Link>
        </div>

        {/* Define Routes */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
