import { useCallback, useEffect, useState } from "preact/hooks";

function useSubscriber(username: string) {
    const [connected, setConnected] = useState<boolean>(false);
    const [messages, setMessages] = useState<string[]>([]);
    const [subscriber, setSubscriber] = useState<EventSource | null>(null);

    const connect = useCallback(() => {
        setConnected(true);
        fetch(`http://localhost:8000/pubsub/connect/${username}`);
    }, []);

    const disconnect = useCallback(() => {
        setConnected(false);
        fetch(`http://localhost:8000/pubsub/disconnect/${username}`);
        subscriber?.close();
        setSubscriber(null);
    }, [subscriber]);

    useEffect(() => {
        connect();
        return () => {
            disconnect();
        };
    }, []);

    useEffect(() => {
        if (connected) {
            setSubscriber(
                new EventSource(
                    `http://localhost:8000/pubsub/subscribe/${username}`
                )
            );
        } else {
            disconnect();
        }
    }, [connected]);

    useEffect(() => {
        if (subscriber) {
            subscriber.onmessage = (event) => {
                setMessages((messages) => [...messages, event.data]);
            };
        }
    }, [subscriber]);

    return { connected, messages };
}

export default useSubscriber;
