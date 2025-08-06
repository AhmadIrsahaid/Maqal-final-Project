import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';

function App() {

const [data, setData] = useState([]);
useEffect(() => {
  axios.get("http://127.0.0.1:8000/api/home").then((respon) => setData(respon.data)).catch(error => console.error(error));
}, []);

  return (
  <div>
    <Navbar/>
      {data ? (
        <>
          <h1>{data.message}</h1>
          <p>{data.content}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
