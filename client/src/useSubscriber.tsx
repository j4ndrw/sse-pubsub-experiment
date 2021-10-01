import { useCallback, useEffect, useState } from "preact/hooks";

function useSubscriber(username: string) {
    const [connected, setConnected] = useState<boolean | null>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [SSE, setSSE] = useState<EventSource | null>(null);

    const connect = useCallback(() => {
        fetch(`http://localhost:8000/pubsub/connect/${username}`);
    }, []);

    const disconnect = useCallback(() => {
        fetch(`http://localhost:8000/pubsub/disconnect/${username}`);
        SSE?.close();
        setSSE(null);
    }, [SSE]);

    useEffect(() => {
        setConnected(true);
        connect();
        return () => {
            setConnected(false);
            disconnect();
        };
    }, []);

    useEffect(() => {
        if (connected !== null) {
            if (connected) {
                setSSE(
                    new EventSource(
                        `http://localhost:8000/pubsub/subscribe/${username}`
                    )
                );
            } else {
                disconnect();
            }
        }
    }, [connected]);

    useEffect(() => {
        if (SSE) {
            SSE.onmessage = (event) => {
                setMessages((messages) => [...messages, event.data]);
            };
        }
    }, [SSE]);

    return { connected, messages };
}

export default useSubscriber;
