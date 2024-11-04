import './Message.css'
import axios from "axios";
import {useNavigate} from "react-router-dom";

export default function Message({message, author, is_own, sent_at, is_superadmin, id, ws}) {
    const navigate = useNavigate();

    async function deleteMessage(messageId) {
        try {
            await axios.delete(`http://localhost:8000/api/messages/${messageId}`,
                {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`},
                },
            )

            ws.send(JSON.stringify({action: 'delete', message_id: messageId}));
        } catch (error) {
            console.log(error);
        }
    }

    async function blockUser(authorId, isOwn) {
        if (isOwn) {
            return false;
        }

        try {
            await axios.post(`http://localhost:8000/api/users/block/${authorId}`, {}, {
                    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`}
                },
            )
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div className={is_own ? `message active` : 'message'}>
            <div className="message-header">
                <h3>{author.username}</h3>
                <button onClick={() => deleteMessage(id)} className={is_superadmin || is_own ? "" : "hidden"}>✘</button>
                <button onClick={() => blockUser(author.id, is_own)} className={is_superadmin ? "" : "hidden"}>⦻
                </button>
            </div>
            <div className="content-time">
                <p>{message}</p>
                <p>{new Date(sent_at).toTimeString().substring(0, 8)}</p>
            </div>
        </div>
    );
}