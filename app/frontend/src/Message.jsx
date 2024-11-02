import './Message.css'

export default function Message({ message, author, is_own, sent_at }) {
    return (
        <div className={is_own ? `message active` : 'message'}>
            <h3>{author}</h3>
            <div className="content-time">
                <p>{message}</p>
                <p>{new Date(sent_at).toTimeString().substring(0, 8)}</p>
            </div>
        </div>
    );
}