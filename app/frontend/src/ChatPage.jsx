import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios from "axios";

export default function ChatPage() {
    const {chatId} = useParams(); // Извлекаем chatId из URL
    const [message, setMessage] = useState(""); // Сообщение для отправки
    const [authStatus, setAuthStatus] = useState(null); // null - загрузка, true - авторизован, false - не авторизован
    const [userId, setUserId] = useState(null);
    const [receivedMessages, setReceivedMessages] = useState([]); // Хранение полученных сообщений
    const [ws, setWs] = useState(null); // Состояние для WebSocket подключения
    const [rendered, setRendered] = useState(false)

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/check-auth", {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                });
                if (response.status === 200) {
                    setAuthStatus(true);
                    setUserId(response.data.id)
                }
            } catch (error) {
                setAuthStatus(false);
            }
        };
        checkAuth();
    }, []);

    // Подключение к WebSocket при монтировании компонента
    useEffect(() => {
        if (authStatus) {
            console.log(`connected to ${chatId} ${userId}`)
            const socket = new WebSocket(`ws://localhost:8000/api/chats/ws/${chatId}/${userId}`); // Подключение к WebSocket серверу

            socket.onopen = () => {
                console.log("WebSocket подключен");
            };

            // socket.onmessage = (event) => {
            //     console.log(event.data);
            //     setReceivedMessages((prevMessages) => [...prevMessages, event.data]); // Добавление нового сообщения в массив
            // };

            socket.onclose = () => {
                console.log("WebSocket отключен");
            };

            setWs(socket); // Сохраняем подключение

            // Закрываем соединение при размонтировании компонента
            return () => {
                socket.close();
            };
        }
    }, [chatId, authStatus]); // обновляем WebSocket подключение при изменении chatId

    useEffect(() => {
        if (authStatus) {
            // setReceivedMessages
            const getMessages = async () => {
                try {
                    setRendered(false);
                    const response = await axios.get(`http://localhost:8000/api/chats/${chatId}`, {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });
                    if (response.status === 200) {
                        console.log(response.data);
                        setReceivedMessages(response.data);
                        setRendered(true);
                    }
                } catch (error) {
                    console.log(error);
                }
            };

            getMessages();
        }
    }, [chatId, authStatus])

    // Отправка сообщения по WebSocket
    const sendMessage = () => {
        if (ws && ws.readyState === WebSocket.OPEN && message.trim()) {
            ws.send(message);
            setMessage("");
        }
    };

    console.log("Rendering with messages:", receivedMessages);

    if (!rendered) {
        return <p>Загрузка...</p>
    }

    return (
        <div>
            <h1>Chat with ID: {chatId}</h1>

            <div>
                <h2>Сообщения</h2>
                <div style={{border: "1px solid #ccc", padding: "10px", minHeight: "200px"}}>
                    {receivedMessages.map(message => (
                        <p key={message.id}>{message.content}</p>
                    ))}
                </div>
            </div>

            <div>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Введите сообщение..."
                />
                <button onClick={sendMessage}>Отправить</button>
            </div>
        </div>
    );
}
