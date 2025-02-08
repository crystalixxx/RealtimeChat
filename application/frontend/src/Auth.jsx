import {useState, useEffect} from 'react';
import {useLocation, Navigate} from 'react-router-dom';
import axios from "axios";

export const setToken = (token) => {
    localStorage.setItem('jwt_token', token);
}

export const fetchToken = () => {
    if (localStorage.getItem('jwt_token') === null) {
        return false;
    }

    const checkAuth = async () => {
        try {
            const response = await axios.get("http://localhost:8000/api/check-auth", {
                headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
            });

            console.log(response.status);
            return response.status === 200;
        } catch (error) {
            return false;
        }
    };

    const ans = checkAuth();
    console.log(ans);
    return checkAuth();
}
