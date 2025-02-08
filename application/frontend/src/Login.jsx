import {useNavigate} from "react-router-dom";
import {fetchToken, setToken} from "./Auth";
import {useEffect, useState} from 'react';
import axios from "axios";
import "./Login.css"

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [authStatus, setAuthStatus] = useState(null);

    const login = (event) => {
        event.preventDefault(); // предотвратить submit формы

        if (!username || !password) {
            console.log("Заполните оба поля");
            return;
        } else {
            const data = new URLSearchParams(); // преобразование данных для form-urlencoded
            data.append("username", username);
            data.append("password", password);

            axios
                .post("http://localhost:8000/api/login", data, {
                    headers: {"Content-Type": "application/x-www-form-urlencoded"}
                })
                .then((response) => {
                    console.log(response.data.access_token, "response.data.access_token");
                    if (response.data.access_token) {
                        setToken(response.data.access_token);
                        navigate("/profile");
                    }
                })
                .catch((error) => {
                    console.error(error, "error");
                });
        }
    };

    useEffect(() => {
        const AuthCheck = async () => {
            const ans = await fetchToken();
            setAuthStatus(ans);
        }

        AuthCheck();
    }, [])

    if (authStatus === null) {
        return <p>loading...</p>
    }

    return (
        <div style={{minHeight: 800, marginTop: 30}}>
            <div style={{marginTop: 30}}>
                {authStatus === true ? (
                    <p>you are logged in</p>
                ) : (
                    <div className="login-container">
                        <form onSubmit={login} className="login-main">
                            <div className="login-title-description">
                                <h2>Войти в аккаунт</h2>
                                <p>Введите данные от вашего аккаунта в поля ниже</p>
                            </div>
                            <div className="login-forms">
                                <input
                                    type="text"
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="Email"
                                />
                                <br/>
                                <input
                                    type="password"
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Password"
                                />
                            </div>
                            <div className="login-additional">
                                <button onClick={() => {
                                    navigate(`/register`)
                                }}>Создать аккаунт</button>
                            </div>
                            <div className="login-submit-container">
                                <button type="submit">Войти</button>
                            </div>
                        </form>
                    </div>
                )}
            </div>
        </div>
    );
}
