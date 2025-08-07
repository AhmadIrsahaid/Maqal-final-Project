import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';

function App() {

const [data, setData] = useState([]);
useEffect(() => {
  axios.get("http://127.0.0.1:8000/api/titile")
    .then((res) => {
      console.log("DATA:", res.data);
      setData(res.data);
    })
    .catch((err) => console.error("ERROR:", err));
}, []);

return (
  <div>
    <Navbar />
    {data.length > 0 ? (
      <div>
        {data.map((item, index) => (
          <h1 key={index}>{item.title}</h1>
        ))}
      </div>
    ) : (
      <p>Loading...</p>
    )}
  </div>
);

}

export default App;
