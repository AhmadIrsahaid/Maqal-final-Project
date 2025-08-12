import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
const Navbar = () => {
  return (
    <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-light" >
        <div className="container px-4 px-lg-5">
          <a className="navbar-brand" href="#!">
            Maqal Panorama
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4">
              <li className="nav-item">
                <Link to={"/"} className="nav-link active" aria-current="page" href="#!">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/About" className="nav-link" href="#!">
                  About
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/articles" className="nav-link" >
                  All Articles
                </Link>
              </li>
              {/*  */}
            </ul>
          
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
