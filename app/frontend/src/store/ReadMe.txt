Store is something that react and redux use to maintain the state for the entire application.
The store is broken up into two parts: the actions and the reducers.
The action is something that we want to define and that takes places.
Inside the actionTypes.js we define all the types of actions that take place: login, logout, etc.
The reducer takes the state and returns only the piece that you need.