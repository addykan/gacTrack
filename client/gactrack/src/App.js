import "./App.css";
import { disableBodyScroll } from "body-scroll-lock";

function App() {
  disableBodyScroll(document);
  return (
    <div className="App">
      <img
        src="https://source.unsplash.com/random/1920x1080"
        height="100%"
        width="100%"
      />
    </div>
  );
}

export default App;
