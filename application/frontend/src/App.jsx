import {Routes, Route} from "react-router-dom";
import Login from "./Login";
import Profile from "./Profile";
import ChatPage from "./ChatPage";

export default function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/profile" element={<Profile/>}/>
                <Route path="/chat/:chatId" element={<ChatPage/>}/>
            </Routes>
        </div>
    )
}
