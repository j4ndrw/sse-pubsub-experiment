import { render } from "preact";
import App from "./app";
import "./index.css";
import { h } from "preact";

const el = document.getElementById("app");
if (el) {
    render(<App />, el);
}
