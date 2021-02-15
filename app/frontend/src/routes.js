import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import ToDoApp from './todo_app/ToDoApp';

function BaseRouter() {
    return (
        <div>
            <Route exact path='/'><Redirect to="/index" /></Route>
            <Route exact path='/index' render={(props) => <ToDoApp  {...props}/>} />
        </div>
    )
};

export default BaseRouter;