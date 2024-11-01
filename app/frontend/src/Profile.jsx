import {useState, useEffect} from "react";
import {redirect, useNavigate} from "react-router-dom";
import axios from "axios";

export default function Profile() {
    const navigate = useNavigate();
    const [authStatus, setAuthStatus] = useState(null); // null - загрузка, true - авторизован, false - не авторизован
    const [username, setUsername] = useState("");
    const [chats, setChats] = useState([]);

    const signOut = () => {
        localStorage.removeItem("jwt_token");
        navigate("/");
    };

    // Проверка аутентификации
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/check-auth", {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                });
                if (response.status === 200) {
                    setAuthStatus(true);
                    setUsername(response.data.username);
                }
            } catch (error) {
                setAuthStatus(false);
            }
        };
        checkAuth();
    }, []);

    // Получение чатов после успешной аутентификации
    useEffect(() => {
        if (authStatus) {
            const getListOfChats = async () => {
                try {
                    const response = await axios.get("http://localhost:8000/api/chats/", {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });
                    if (response.status === 200) {
                        setChats(response.data.chats);
                    }
                } catch (error) {
                    console.log(error);
                }
            };
            getListOfChats();
        }
    }, [authStatus]); // запускается только если authStatus изменился на true

    // Проверка статуса авторизации
    if (authStatus === null) {
        return <p>Загрузка...</p>;
    }

    if (authStatus === false) {
        return <p>Ресурс недоступен, обновите токен</p>;
    }

    return (
        <div style={{marginTop: 20, minHeight: 700}}>
            <h1>Profile page</h1>
            <p>Hello {username}, welcome to your profile page</p>
            <p>Number of chats: {chats.length}</p>

            <button onClick={signOut}>sign out</button>

            {chats.map((chat, index) => (
                <button key={index} onClick={() => {
                    navigate(`/chat/${chat.id}`)
                }} style={{backgroundColor: "red"}}>
                    <p>{chat.id}</p>
                    <p>{chat.name}</p>
                </button>
            ))}
        </div>
    );
}
