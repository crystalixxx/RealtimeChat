import { useState, useEffect } from 'react';
import { useLocation, Navigate } from 'react-router-dom';

export const setToken = (token) => {
    localStorage.setItem('jwt_token', token);
}

export const fetchToken = () => {
    return localStorage.getItem('jwt_token');
}
