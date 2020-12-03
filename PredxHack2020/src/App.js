import React,{useEffect} from 'react';
import {Router,Route,Redirect,Switch} from 'react-router-dom'
import {history} from './helpers/history'
import {useSelector,useDispatch} from 'react-redux'
import './App.css';
import {clearErrors} from './redux/actions/errorActions'
import {loadUser} from './redux/actions/authAction'
import Auth from './components/Auth/Auth'
import { useState } from 'react';



function App() {

  const dispatch = useDispatch()
   history.listen((location, action) => {
    // clear alert on location change
    dispatch(clearErrors())
  });
  useEffect(()=>{
    dispatch(loadUser())
  },[])

  console.log("rerendering")
 
  return (
    <div className='app'>
        <div className='main-body'>
        <Router history={history}>
          <Switch>
                <Route exact path="/" >
                    <Auth/>
                </Route>
                <Route path="/register">
                    <Auth/>
                </Route>
                <Route path="/login">
                    <Auth/>
                </Route>
            </Switch>
            </Router>
        </div>
    </div>
  );
}

export default App;
