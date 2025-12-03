import './Navbar.css'

import { useState } from "react";
import "./Navbar.css";   // You will paste the CSS I give next

export default function NavigationBar() {
  const [open, setOpen] = useState(false);

  const navItems = [
    { label: "Home", href: "/" },
    { label: "Players", href: "/players" },
    { label: "Leagues", href: "/leagues" },
    { label: "My Team", href: "/team" },
    { label: "Transfers", href: "/transfers" },
    { label: "Week Points", href: "/points" },
    { label: "Login", href: "/login" },
  ];

  return (
    <header className="navbar">
      <div className="nav-left">
        <div className="logo">Fantasy NWSL</div>

        {/* Hamburger button */}
        <button
          className="hamburger"
          onClick={() => setOpen(!open)}
          aria-label="Toggle Menu"
        >
          ☰
        </button>

        {/* Navigation Links (desktop + mobile) */}
        <nav className={`nav-links ${open ? "open" : ""}`}>
          {navItems.map((item) => (
            <a key={item.href} href={item.href}>
              {item.label}
            </a>
          ))}
        </nav>
      </div>
    </header>
  );
}



function PageHeader() {
  return (
      <head>
        <meta charset="UTF-8"></meta>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
        <title>Fantasy NWSL</title>
        <meta name="author" content="Levi Hauck"></meta>
        <link rel="stylesheet" type="text/css" href="/Fantasy-NWSL/app/static/css/style.css"></link>
      </head>
  );
}


function PageFooter() {
  return (
    <footer>
    <p> Fantasy NWSL&trade;</p>
    </footer>
  )
}

export {NavigationBar, PageFooter, PageHeader};