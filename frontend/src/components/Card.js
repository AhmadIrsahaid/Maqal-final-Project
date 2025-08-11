import axios from "axios";
import { useState, useEffect } from "react";

function Card() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/card")
      .then((res) => {
        console.log("DATA:", res.data);
        setData(res.data);
      })
      .catch((err) => console.error("ERROR:", err));
  }, []); // ✅ Added [] so it runs only once

  return (
    <div className="container mt-5">
      <h1 className="mb-4 text-center">Hello from Card</h1>
      {data.length > 0 ? (
        <div className="row g-4">
          {data.map((item, index) => (
            <div key={index} className="col-md-4"> 
              <div className="card h-100">
                <img
                  src="https://via.placeholder.com/300x200"
                  className="card-img-top"
                  alt={item.title}
                />
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title">{item.title}</h5>
                  <p className="card-text">{item.content}</p>
                  <a href="#" className="btn btn-primary mt-auto">
                    Go somewhere
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Card;
