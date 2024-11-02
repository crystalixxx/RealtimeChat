import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios from "axios";
import './ChatPage.css'
import Message from "./Message.jsx";

export default function ChatPage() {
    const {chatId} = useParams();
    const [message, setMessage] = useState("");
    const [authStatus, setAuthStatus] = useState(null);
    const [userId, setUserId] = useState(null);
    const [receivedMessages, setReceivedMessages] = useState([]);
    const [ws, setWs] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/check-auth", {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                });
                if (response.status === 200) {
                    setAuthStatus(true);
                    setUserId(response.data.id);
                }
            } catch (error) {
                setAuthStatus(false);
            }
        };
        checkAuth();
    }, []);

    useEffect(() => {
        if (authStatus) {
            const socket = new WebSocket(`ws://localhost:8000/api/chats/ws/${chatId}/${userId}`);

            socket.onopen = () => {
                console.log("WebSocket подключен");
            };

            socket.onmessage = (event) => {
                console.log(`New message: ${event.data}`);
                handleMessages();
            }

            socket.onclose = () => {
                console.log("WebSocket отключен");
            };

            setWs(socket);

            return () => {
                socket.close();
            };
        }
    }, [chatId, authStatus]);

    async function handleMessages() {
        try {
            const response = await axios.get(`http://localhost:8000/api/chats/${chatId}`, {
                headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
            });
            if (response.status === 200) {
                setReceivedMessages(response.data.sort((a, b) => {
                    return -(new Date(b.sent_at) - new Date(a.sent_at));
                }));
            }
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        if (authStatus) {
            handleMessages();
        }
    }, [chatId, authStatus]);

    useEffect(() => {
        const messagesContainer = document.querySelector('.messages-storage');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }, [receivedMessages]);

    const sendMessage = () => {
        if (ws && message.trim()) {
            ws.send(message);
            setMessage("");
        }
    };

    return (
        <div className="message-container">
            <h1>Chat with ID: {chatId}</h1>

            <div className="messages-storage">
                {receivedMessages.map((msg, index) => (
                    <Message key={index} message={msg.content} author={msg.sender.username}
                             is_own={msg.sender_id == userId} sent_at={msg.sent_at}/>
                ))}
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
