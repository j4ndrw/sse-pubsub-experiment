import { useCallback, useEffect, useState } from "preact/hooks";

interface Subscriber {
    connectURL: string;
    subscribeURL: string;
    disconnectURL: string;
}

function useSubscriber({
    connectURL,
    subscribeURL,
    disconnectURL,
}: Subscriber) {
    const [connected, setConnected] = useState<boolean | null>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [SSE, setSSE] = useState<EventSource | null>(null);

    const connect = useCallback(() => {
        fetch(connectURL);
        setConnected(true);
    }, [connected]);

    const disconnect = useCallback(() => {
        fetch(disconnectURL);
        setConnected(false);
    }, [connected]);

    useEffect(() => {
        connect();
        return () => {
            disconnect();
        };
    }, []);

    useEffect(() => {
        if (connected !== null) {
            setSSE((SSE) => {
                if (!connected) {
                    disconnect();
                    SSE?.close();
                    return null;
                }
                return new EventSource(subscribeURL);
            });
        }
    }, [connected]);

    useEffect(() => {
        if (SSE)
            SSE.onmessage = (event) =>
                setMessages((messages) => [...messages, event.data]);
    }, [SSE]);

    return { connected, messages, connect, disconnect };
}

export default useSubscriber;
