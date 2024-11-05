import {useState, useEffect} from "react";
import {redirect, useNavigate} from "react-router-dom";
import axios from "axios";
import './Profile.css'
import Modal from "react-modal";

export default function Profile() {
    const navigate = useNavigate();
    const [authStatus, setAuthStatus] = useState(null);
    const [username, setUsername] = useState("");
    const [chats, setChats] = useState([]);
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [commonUsers, setCommonUsers] = useState([]);
    const [chatName, setChatName] = useState("");

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    Modal.setAppElement("#root");

    const signOut = () => {
        localStorage.removeItem("jwt_token");
        navigate("/");
    };

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

    useEffect(() => {
        if (authStatus) {
            const getListOfChats = async () => {
                try {
                    const response = await axios.get("http://localhost:8000/api/chats/", {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });
                    if (response.status === 200) {
                        setChats(response.data);
                    }
                } catch (error) {
                    console.log(error);
                }
            };
            getListOfChats();
        }
    }, [authStatus]);

    useEffect(() => {
        if (authStatus) {
            const getListOfCommonUsers = async () => {
                try {
                    const response = await axios.get("http://localhost:8000/api/users/common", {
                        headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                    });
                    if (response.status === 200) {
                        setCommonUsers(response.data);
                    }
                } catch (error) {
                    console.log(error);
                }
            };
            getListOfCommonUsers();
        }
    }, [authStatus]);

    if (authStatus === null) {
        return <p>Загрузка...</p>;
    }

    const customStyles = {
        content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
            width: '25vw',
            height: '80vh',
        },
    };

    async function createNewChat(userId, chatName) {
        try {
            await axios.post(`http://localhost:8000/api/chats/${userId}`,
                {name: chatName},
                {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                },
            ).then(_ => {
                closeModal()
                navigate(0)
            });


        } catch (error) {
            console.log(error);
        }
    }

    const modalContent = (
        <div className="create-new-chat-modal">
            <div className="modal-main-content">
                <h2>Выберите с кем создать чат</h2>

                <input type="text"
                       value={chatName}
                       onChange={(e) => setChatName(e.target.value)}
                       placeholder="Введите сообщение..."/>

                <div className="modal-users-list-container">
                    {commonUsers.map((user, index) => {
                        return <div key={index} className="users-add-content-div">
                            <p>{user.username}</p>
                            <button onClick={() => createNewChat(user.id, chatName)}>X</button>
                        </div>
                    })}
                </div>
            </div>
            <div className="modal-down-content">
                <button onClick={closeModal} className="modal-close-button">X</button>
            </div>
        </div>
    );

    return (
        <div className="profile-container">
            <div className="profile">
                <div className="profile-action-header">
                    <ul>
                        <li>
                            <button onClick={signOut}>Выйти</button>
                        </li>
                        <li>
                            <button onClick={openModal}>Новый чат</button>

                            <Modal isOpen={modalIsOpen}
                                   onRequestClose={closeModal}
                                   style={customStyles}
                                   contentLabel="Создать новый чат">
                                {modalContent}
                            </Modal>
                        </li>
                    </ul>
                </div>
                <div className="profile-info-container">
                    <h1>{username}</h1>
                    <p>Количество чатов: {chats.length}</p>
                </div>
                <div className="profile-chats">
                    {chats.map((chat, index) => (
                        <button key={index} onClick={() => {
                            navigate(`/chat/${chat.id}`)
                        }}>{chat.name} (#{chat.id})</button>
                    ))}
                </div>
            </div>
        </div>
    );
}
