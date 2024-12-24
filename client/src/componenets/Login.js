import React, { useState } from 'react';
import { login } from '../services/api';
import { useNavigate } from 'react-router-dom'; // useNavigate is now the correct hook

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [welcomeMessage, setWelcomeMessage] = useState('');
  const [role, setRole] = useState('');
  const navigate = useNavigate(); // useNavigate hook for redirection

  const handleLogin = async () => {
    try {
      const response = await login({ username, password });
      console.log(response.data);
  
      // decoding the ID token (JWT) to extract groups (roles)
      const idToken = response.data.id_token;
      const decodedToken = JSON.parse(atob(idToken.split('.')[1])); // decode the JWT
  
      // log the decoded token to inspect its structure
      console.log("Decoded Token:", decodedToken);
  
      const roles = decodedToken['cognito:groups'] || []; // get the groups (roles) assigned
      const email = decodedToken['email']; // extract the email from the decoded token - to display correct tasks for logged in user
  
      const userRole = roles.includes('Admin') ? 'Admin' : 'NormalUser'; // Check if user is in 'Admin' or 'NormalUser' group
  
      localStorage.setItem('role', userRole); // storing the role
      localStorage.setItem('username', username); // saving username to localStorage
      localStorage.setItem('email', email); // saving email to localStorage
  
      console.log("Logged-in user email:", email);
  
      // setting the role and welcome message
      setRole(userRole);
      setWelcomeMessage(`Welcome ${username} - ${userRole}`);
    } catch (error) {
      setErrorMessage('Login failed: ' + (error.response?.data?.message || error.message));
    }
  };
  

  const goToDashboard = () => {
    if (role === 'Admin') {
      navigate('/admin-dashboard');
    } else if (role === 'NormalUser') {
      navigate('/user-dashboard');
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <button onClick={handleLogin}>Login</button>

      {/* display the welcome message after successful login */}
      {welcomeMessage && <p className="welcome-message">{welcomeMessage}</p>}

      {/* display the button to navigate to the appropriate dashboard BASED ON ROLE */}
      {role && (
        <button onClick={goToDashboard}>Go to {role} Dashboard</button>
      )}
    </div>
  );
};

export default Login;
