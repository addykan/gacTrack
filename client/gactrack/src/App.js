import "./App.css";
import { disableBodyScroll } from "body-scroll-lock";
import Time from "./components/Time";
import { Grid } from "@material-ui/core";

function App() {
  disableBodyScroll(document);
  return (
    <div
      className="App"
      style={{
        backgroundImage: "url('https://source.unsplash.com/random/1920x1080')",
        height: "100vh",
      }}
    >
      <Time />
    </div>
  );
}

export default App;
