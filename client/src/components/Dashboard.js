import React, { useState } from 'react';
import { creatTask } from '../services/api';


const Dashboard = () => {
const [task,setTask] = useState ({title: '',description: '', deadline: '', assigned: ''});

const handle_T_Creation = async () => {
const response = await creatTask(task);
console.log(response.data);
};

return (
<div>
<input type="text" placeholder="Title" onChange={ (e) => setTask({...task, title: e.target.value})} />

<input type="text" placeholder="Description" onChange={ (e) => setTask({...task, description: e.target.value})} />

<input type="text" placeholder="Deadline" onChange={ (e) => setTask({...task, deadline: e.target.value})} />

<input type="text" placeholder="Assigned To" onChange={ (e) => setTask({...task, assigned: e.target.value})} />

<button onClick={handle_T_Creation}>Create Task</button>
</div>
);
};
export default Dashboard;