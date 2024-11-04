import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import axios from "axios";
import './ChatPage.css'
import Message from "./Message.jsx";
import Modal from 'react-modal';

export default function ChatPage() {
    const navigate = useNavigate();
    const {chatId} = useParams();
    const [message, setMessage] = useState("");
    const [authStatus, setAuthStatus] = useState(null);
    const [chatData, setChatData] = useState({});
    const [userId, setUserId] = useState(null);
    const [isSuperadmin, setIsSuperadmin] = useState(false);
    const [receivedMessages, setReceivedMessages] = useState([]);
    const [ws, setWs] = useState(null);
    const [usersToAdd, setUsersToAdd] = useState([]);
    const [currentUsers, setCurrentUsers] = useState([]);
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const openModal = () => {
        getUserToAddData();
        getCurrentUserData();
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    async function getCurrentUserData() {
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

    async function getUserToAddData() {
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

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/check-auth", {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                });
                if (response.status === 200) {
                    setAuthStatus(true);
                    setUserId(response.data.id);
                    setIsSuperadmin(response.data.is_superadmin);
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

    async function deleteChat() {
        try {
            const response = await axios.delete(`http://localhost:8000/api/chats/${chatId}`, {
                headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
            })

            if (response.status === 200) {
                navigate(`/profile`);
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function removeFromChat(deletingUserId) {
        if (userId !== deletingUserId && !isSuperadmin) {
            return false;
        }

        try {
            const response = await axios.put(`http://localhost:8000/api/chats/${chatId}/${deletingUserId}`, {},
                {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                })

            if (response.status === 200) {
                if (userId === deletingUserId) {
                    navigate("/profile");
                } else {
                    navigate(0);
                }
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function addMemberToChat(userId) {
        try {
            const response = await axios.post(`http://localhost:8000/api/chats/${chatId}/${userId}`, {},
                {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                })

            console.log(response.status, response.data);
            if (response.status === 200) {
                navigate(0);
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
            ws.send(JSON.stringify({action: 'send', message: {text: message}}));
            setMessage("");
        }
    };

    Modal.setAppElement("#root");

    const modalContent = (
        <div className="main-modal-users-add">
            <button onClick={closeModal} className="modal-close-button">X</button>

            <h1>New Users to Add</h1>
            <div className="users-to-add-list">
                {usersToAdd.map((user, index) => {
                    return <div key={index} className="users-add-content-div">
                        <p>{user.username}</p>
                        <button onClick={() => addMemberToChat(user.id)}>+</button>
                    </div>
                })}
            </div>

            <h1>Users List</h1>
            <div className="second-div">
                {currentUsers.map((user, index) => {
                    return <div key={index} className="users-add-content-div">
                        <p>{user.username}</p>
                        <button onClick={() => removeFromChat(user.id)} className={isSuperadmin ? "" : "hidden"}>X</button>
                    </div>
                })}
            </div>
        </div>
    );

    return (
        <div className="message-container">
            <div className="header">
                <button onClick={() => removeFromChat(userId)} className={isSuperadmin ? "hidden" : ""}>Выйти</button>
                <button onClick={openModal} className="header-h1-button">{chatData.name}</button>
                <button onClick={deleteChat} className={isSuperadmin ? 'remove-button' : 'remove-button hidden'}>
                    Удалить
                </button>
            </div>

            <Modal isOpen={modalIsOpen} onRequestClose={closeModal}>
                {modalContent}
            </Modal>

            <div className="messages-storage">
                {receivedMessages.map((msg, index) => (
                    <Message key={index} message={msg.content} author={msg.sender}
                             is_own={msg.sender_id === userId} sent_at={msg.sent_at} is_superadmin={isSuperadmin}
                             id={msg.id} ws={ws}/>
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
