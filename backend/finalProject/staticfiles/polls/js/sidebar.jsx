
import './style.css'
const Sidebar = () => {
  const [isExpanded, setIsExpanded] = React.useState(false);

  const menuItems = [
    { href: "/home", iconClass: "lni lni-home", label: "Home" },
    { href: "/ProfilePage", iconClass: "lni lni-user", label: "Profile" },
    { href: "/myorder", iconClass: "lni lni-layers", label: "My Orders" },
    { href: "#/", iconClass: "lni lni-map-marker", label: "Billing Address" },
  ];

  return (
    <div className={`wrapper ${isExpanded ? "expanded" : ""}`}>
      <aside id="sidebar">
        <div className="d-flex">
          <button className="toggle-btn" type="button">
            <i className="lni lni-grid-alt"></i>
          </button>
          <div className="sidebar-logo">
            {/* remove the logo import and use a normal <img> URL/static later */}
            <img src="#" alt="" className="" />
          </div>
        </div>
        <ul className="vstack p-0">
          {menuItems.map((item, index) => (
            <li className="sidebar-item" key={index}>
              <a href={item.href} className="sidebar-link">
                <i className={item.iconClass}></i>
                <span>{item.label}</span>
              </a>
            </li>
          ))}
        </ul>
        <div className="sidebar-footer">
          <a href="#" className="sidebar-link">
            <i className="lni lni-exit"></i>
            <span>Sign out</span>
          </a>
        </div>
      </aside>
    </div>
  );
};

// Render it inside root div
ReactDOM.render(<Sidebar />, document.getElementById("root"));
