import './App.css';
import Card from './components/Card';
import { Routes, Route, Link } from "react-router-dom";
// import { useState, useEffect } from 'react';
// import axios from 'axios';
import Navbar from './components/Navbar';
import About from './pages/About';
import Home from './pages/Home';

function App() {

// const [data, setData] = useState([]);
// useEffect(() => {
//   axios.get("http://127.0.0.1:8000/api/titile")
//     .then((res) => {
//       console.log("DATA:", res.data);
//       setData(res.data);
//     })
//     .catch((err) => console.error("ERROR:", err));
// }, []);

return (
  <div>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/articles" element={<Card />} />
      <Route path="/About" element={<About/>} />
      {/* Add other routes here as needed */}
    </Routes>
    {/* <Navbar /> */}
    {/* <Card/> */}
  </div>
);

}

export default App;
