import React from "react";
import { Route, Switch, NavLink } from "react-router-dom";

// pages
import HomePage from "./pages/HomePage";
import IndexesPage from "./pages/IndexesPage";
import CardPage from "./pages/CardPage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";


const Header = () => {
  return (
    <header>
      <nav className="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a className="navbar-brand" href="#">T1M</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarCollapse">
          <ul className="navbar-nav mr-auto">
            <li>
              <NavLink className="nav-link" to="/">Home</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/indexes">Indexes</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/about">About</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/contact">Contact</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/cards">(Card)</NavLink>
            </li>
          </ul>
          <form className="form-inline mt-2 mt-md-0">
            <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />
            <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form>
        </div>
      </nav>
    </header>
  )
}

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <span className="text-muted"><small>Copyright (c) 2020, Tier1Marketspace</small></span>
      </div>
    </footer>
  )
}

const App = () => {
  return (
    <>
      <Header/>
      <main role="main" className="container">
        <Switch>
          <Route exact path="/" component={HomePage}/>
          <Route exact path="/indexes" component={IndexesPage}/>
          <Route exact path="/about" component={AboutPage}/>
          <Route exact path="/contact" component={ContactPage}/>
          <Route exact path="/cards" component={CardPage}/>
        </Switch>
      </main>
      <Footer/>
    </>
  )
}
 
export default App;
