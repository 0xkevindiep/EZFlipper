import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import 'bootstrap/dist/css/bootstrap.css';

class Doc extends React.Component{
    componentDidMount(){
        document.title = "Kash Machine"
    }
  
    render(){
        return(
            <div></div>
        )
    }
}

ReactDOM.render(
  <React.StrictMode>
    <Doc />
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Offline - serviceWorker.register(); 
// Online - serviceWorker.unregister(); 
serviceWorker.register();