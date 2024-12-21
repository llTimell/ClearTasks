import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './componenets/Login';
import Register from './componenets/Register';
import AdminDashboard from './componenets/AdminDashboard';  
import UserDashboard from './componenets/UserDashboard';   
import './App.css';

function App() {
  return (
    <Router>
      <div style={{ textAlign: 'center', margin: '20px' }}>
        <h1>ClearTasks Cloud Project</h1>
        {/* navigation buttons */}
        <div className="nav-buttons">
          <Link to="/login" className="link-button">
            Login
          </Link>
          <Link to="/register" className="link-button">
            Register
          </Link>
        </div>

        {/* defining the Routes */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} /> {/* admin dashboard route */}
          <Route path="/user-dashboard" element={<UserDashboard />} /> {/* aser dashboard route */}
          {/*last two routes depend on role */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
