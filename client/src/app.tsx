import { h } from "preact";
import useSubscriber from "./useSubscriber";
import { v4 } from "uuid";

const USERNAME = `John Doe ${v4()}`;

const api = (endpoint: string) => `http://localhost:8000/pubsub/${endpoint}`;

function App() {
    const { messages } = useSubscriber({
        connectURL: api(`connect/${USERNAME}`),
        subscribeURL: api(`subscribe/${USERNAME}`),
        disconnectURL: api(`disconnect/${USERNAME}`),
    });

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <div>
                <h1>Messages</h1>
                <div>
                    {messages.map((message) => (
                        <p>{message}</p>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
