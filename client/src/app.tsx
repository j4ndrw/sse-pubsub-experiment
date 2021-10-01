import { h } from "preact";
import useSubscriber from "./useSubscriber";
import { v4 } from "uuid";

function App() {
    const { messages } = useSubscriber(`John Doe ${v4()}`);

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
