import React, { useState, useEffect } from 'react';

const UserDashboard = () => {
  const [task, setTask] = useState({ title: '', description: '', deadline: '' });
  const [tasks, setTasks] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'NormalUser') {
      window.location.href = '/login'; // redirect if not NormalUser
    }
  }, []);

  const handleUpdateTaskStatus = (taskId) => {
    // to update task status, e.g., "In Progress" or "Completed"
    const updatedTasks = tasks.map((t) =>
      t.id === taskId ? { ...t, status: 'Completed' } : t
    );
    setTasks(updatedTasks);
  };

  return (
    <div className="container">
      <h2>User Dashboard</h2>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {/* list of created or assigned tasks -- missing implemenation */}
      <h3>Your Tasks:</h3>
      {tasks.length === 0 ? (
        <p>No tasks available.</p>
      ) : (
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>
              <strong>{task.title}</strong> - Deadline: {task.deadline}
              <button onClick={() => handleUpdateTaskStatus(task.id)}>Mark as Completed</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default UserDashboard;
