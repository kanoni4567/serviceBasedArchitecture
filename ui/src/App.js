import React from 'react';
import { makeStyles } from "@material-ui/core/styles";
import logo from './logo.svg';
import './App.css';

import DataCard from './components/DataCard'

const useStyles = makeStyles({
  root: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px 40px',
    backgroundColor: '#2a7886'
  }
});

function App() {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <div>
        <img src="/sell-link-buy.png" className="App-logo" alt="logo" />
      </div>
      <DataCard></DataCard>
    </div>
  );
}

export default App;
