import { useNavigate } from "react-router-dom";
import { fetchToken, setToken } from "./Auth";
import { useState } from 'react';
import axios from "axios";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

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
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then((response) => {
          console.log(response.data.access_token, "response.data.access_token");
          if (response.data.access_token) {
            setToken(response.data.access_token); // убедитесь, что setToken определен
            navigate("/profile");
          }
        })
        .catch((error) => {
          console.error(error, "error");
        });
    }
  };

  return (
    <div style={{ minHeight: 800, marginTop: 30 }}>
      <h1>login page</h1>
      <div style={{ marginTop: 30 }}>
        {fetchToken() ? (
          <p>you are logged in</p>
        ) : (
          <div>
            <form onSubmit={login}>
              <label style={{ marginRight: 10 }}>Input Username</label>
              <input
                type="text"
                onChange={(e) => setUsername(e.target.value)}
              />

              <label style={{ marginRight: 10 }}>Input Password</label>
              <input
                type="password"
                onChange={(e) => setPassword(e.target.value)}
              />

              <button type="submit">Login</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
