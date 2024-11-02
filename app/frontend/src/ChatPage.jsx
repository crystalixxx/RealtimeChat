import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios from "axios";
import './ChatPage.css'
import Message from "./Message.jsx";
import Modal from 'react-modal';

export default function ChatPage() {
    const {chatId} = useParams();
    const [message, setMessage] = useState("");
    const [authStatus, setAuthStatus] = useState(null);
    const [chatData, setChatData] = useState({});
    const [userId, setUserId] = useState(null);
    const [receivedMessages, setReceivedMessages] = useState([]);
    const [ws, setWs] = useState(null);
    const [usersToAdd, setUsersToAdd] = useState([]);
    const [currentUsers, setCurrentUsers] = useState([]);
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

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
            const getChatData = async () => {
                try {
                    const response = await axios.get(`http://localhost:8000/api/chats/${chatId}`, {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });

                    if (response.status === 200) {
                        setChatData(response.data);
                    }
                } catch (error) {
                    setAuthStatus(false);
                }
            };

            getChatData();
        }
    }, [authStatus, chatId]);

    useEffect(() => {
        if (authStatus) {
            const getUserToAddData = async () => {
                try {
                    const response = await axios.get(`http://localhost:8000/api/chats/available_users/${chatId}`, {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });

                    if (response.status === 200) {
                        setUsersToAdd(response.data);
                    }
                } catch (error) {
                    setAuthStatus(false);
                }
            }

            const getCurrentUserData = async () => {
                try {
                    const response = await axios.get(`http://localhost:8000/api/chats/members/${chatId}`, {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    })

                    if (response.status === 200) {
                        setCurrentUsers(response.data)
                    }
                } catch (error) {
                    setAuthStatus(false);
                }
            }

            getUserToAddData();
            getCurrentUserData();
        }
    }, [chatId, authStatus])

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
            const response = await axios.get(`http://localhost:8000/api/chats/messages/${chatId}`, {
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

    async function addMemberToChat(userId) {
        try {
            const response = await axios.post(`https://localhost:8000/api/chats/${chatId}/${userId}`, {
                headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
            })
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

    Modal.setAppElement("#root");

    const modalContent = (
        <div className="main-modal-users-add">
            <button onClick={closeModal} className="modal-close-button">X</button>

            <div className="second-div">
                {currentUsers.map((user, index) => {
                    return <div key={index} className="users-add-content-div">
                        <p>{user.username}</p>
                        <button>X</button>
                    </div>
                })}
            </div>

            <p>AHASHAHSHAS</p>

            <div className="users-to-add-list">
                {usersToAdd.map((user, index) => {
                    return <div key={index} className="users-add-content-div">
                        <p>{user.username}</p>
                        <button>+</button>
                    </div>
                })}
            </div>
        </div>
    );

    return (
        <div className="message-container">
            <div className="header">
                <h1>{chatData.name}</h1>
                <button className="add-user-button" onClick={openModal}>
                    +
                </button>
            </div>

            <Modal isOpen={modalIsOpen} onRequestClose={closeModal}>
                {modalContent}
            </Modal>

            <div className="messages-storage">
                {receivedMessages.map((msg, index) => (
                    <Message key={index} message={msg.content} author={msg.sender.username}
                             is_own={msg.sender_id == userId} sent_at={msg.sent_at}/>
                ))}
            </div>

            <div className="input-container">
                <div className="input-wrapper">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Введите сообщение..."
                        className="message-input"
                    />
                </div>
                <button onClick={sendMessage} className="message-send-button">Отправить</button>
            </div>
        </div>
    );
}
