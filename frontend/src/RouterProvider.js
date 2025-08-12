import {
  createBrowserRouter,
  RouterProvider,
} from "react-router";

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Card from "./components/Card";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },
  {
    path : "/articles",
    element: <Card/>
  }
]);

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <RouterProvider router={router} />,
);
