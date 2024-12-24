import React, { useState, useEffect } from 'react';
import { getTasks, updateTaskStatus } from '../services/api';

const UserDashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'NormalUser') {
      window.location.href = '/login'; // redirect if not NormalUser
    }

    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await getTasks();
      const email = localStorage.getItem('email'); // get the email of the logged-in user - to compare with "assigned to"
      console.log("logged-in user email:", email); // log logged-in user email

      // filter tasks based on whether the user is assigned to or created the task
      const filteredTasks = response.tasks.filter(task => 
        task.assigned_to === email || task.created_by === email
      );

      setTasks(filteredTasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setError('Failed to load tasks. Please try again later.');
    }
  };

  const handleUpdateTaskStatus = async (title) => {
    try {
      await updateTaskStatus(title, 'completed');
      fetchTasks();
    } catch (error) {
      console.error(`Error updating task status for ${title}:`, error);
      setError(`Failed to update status for ${title}.`);
    }
  };

  return (
    <div className="container">
      <h2>User Dashboard</h2>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h3>Your Tasks:</h3>
      {tasks.length === 0 ? (
        <p>No tasks available.</p>
      ) : (
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>
              <strong>{task.title}</strong> - {task.description}, Deadline: {task.deadline}, Status: {task.status || 'Not Started'}
              {task.status !== 'completed' && (
                <button onClick={() => handleUpdateTaskStatus(task.title)}>Mark as Completed</button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default UserDashboard;
