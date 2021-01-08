import React, {Component} from 'react';
import '../css/parent.css';
import logo from '../img/logo.png';

class NavBar extends Component {
    render() {
        return (
            <header>
            <nav className="navbar navbar-expand-lg navbar-dark">
                <div className= "container nav-inner">
                <img src={logo} className="header-icon" alt="Logo"></img>
                <a className="navbar-brand" href="/">Kash Machine</a>
                <button className="navbar-toggler" type="button"  data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <a className="nav-link" href="/">Home</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="/about">About</a>
                        </li>
                    </ul>
                </div>
                </div>
            </nav>
            </header>
        );
    }
}

export default NavBar;