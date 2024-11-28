import React, { useState } from 'react';
import { login } from '../services/api';

const Login = () => {
    const [username, setUername] = useState('');
    const [password, setPassword] = useState('');
    const handleLogin = async () => {
        const response = await login({username, password});
        console.log(response.data);
       
    };

    return(
        <div>
        <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;