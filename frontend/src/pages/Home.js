import React, { Component } from "react";
import "../css/index.css";
import NavBar from "../components/navBar.js";

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ""
        }
    }
    render() {
        return(
            <div>
                <NavBar />
            </div>
        )
    }
}

export default Home;