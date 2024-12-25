import React, { useState, useEffect } from 'react';
import { createTask, getTasks, deleteTask } from '../services/api';

const AdminDashboard = () => {
  const [task, setTask] = useState({ title: '', description: '', deadline: '', assigned_to: '', created_by: '', priority: '' });
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const role = localStorage.getItem('role');
    if (role !== 'Admin') {
      window.location.href = '/login'; // redirect if not Admin
    }
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await getTasks();
      setTasks(response.tasks); // admin sees all tasks
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const handleCreateTask = async () => {
    try {
      const createdBy = localStorage.getItem('username');
      const newTask = { ...task, created_by: createdBy };
      await createTask(newTask);
      fetchTasks();
      setTask({ title: '', description: '', deadline: '', assigned_to: '', created_by: '', priority: '' });
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

const handleDeleteTask = async (title) => {
  try {
    await deleteTask(title);
  } catch (error) {
    alert("Failed to delete task.");
  }
};

  return (
    <div className="container">
      <h2>Admin Dashboard</h2>
      <div className="task-form">
        <input
          type="text"
          placeholder="Title"
          value={task.title}
          onChange={(e) => setTask({ ...task, title: e.target.value })}
          className="input-field"
        />
        <textarea
          placeholder="Description"
          value={task.description}
          onChange={(e) => setTask({ ...task, description: e.target.value })}
          className="input-field"
        />
        <input
          type="date"
          value={task.deadline}
          onChange={(e) => setTask({ ...task, deadline: e.target.value })}
          className="input-field"
        />
        <input
          type="text"
          placeholder="Assigned To"
          value={task.assigned_to}
          onChange={(e) => setTask({ ...task, assigned_to: e.target.value })}
          className="input-field"
        />
        
        <select
          value={task.priority}
          onChange={(e) => setTask({ ...task, priority: e.target.value })}
          className="input-field"
        >
          <option value="">Priority</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
        
        <button onClick={handleCreateTask} className="submit-button">Create Task</button>
      </div>

      <h3>Task List</h3>
      <ul>
        {tasks.map((task, index) => (
          <li key={index} className="task-item">
            <strong>{task.title}</strong> - Assigned to: {task.assigned_to}, Deadline: {task.deadline}
            <button onClick={() => handleDeleteTask(task.title)} className="delete-button">Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminDashboard;
