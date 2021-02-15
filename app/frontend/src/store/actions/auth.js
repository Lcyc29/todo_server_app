// WE are going to define the methods that will take place upon receiving those actions
import * as actionTypes from './actionTypes';
// import axios from 'axios';

export const authStart = () => {
    return {
        type: actionTypes.AUTH_START// when working with actions, the object that we need to return always have to include a type.
    };
};