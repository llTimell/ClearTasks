import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [task, setTask] = useState({ title: '', description: '', deadline: '', assignedTo: '' });
  const [tasks, setTasks] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'Admin') {
      window.location.href = '/login'; // redirect if not Admin
    }
  }, []);

  return (
    <div className="container">
      <h2>Admin Dashboard</h2>

      {/* task Creation Form -- missing implementation */}

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {/* list of created tasks -- missing implementation*/}
      <h3>Task List:</h3>
      {tasks.length === 0 ? (
        <p>No tasks created yet.</p>
      ) : (
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>
              <strong>{task.title}</strong> - Assigned to: {task.assignedTo}, Deadline: {task.deadline}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdminDashboard;
