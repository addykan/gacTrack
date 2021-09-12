import "./App.css";
import { disableBodyScroll } from "body-scroll-lock";
import Time from "./components/Time";
import { Grid, createMuiTheme, ThemeProvider } from "@material-ui/core";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#ffffffff",
    },
  },
});

function App() {
  disableBodyScroll(document);
  return (
    <ThemeProvider theme={theme}>
      <div
        className="App"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), url('https://source.unsplash.com/random/1920x1080')",
        }}
      >
        <Grid
          container
          spacing={2}
          alignItems="center"
          justify="center"
          style={{ minHeight: "100vh" }}
        >
          <Grid item xs={12}>
            <Time />
          </Grid>
        </Grid>
      </div>
    </ThemeProvider>
  );
}

export default App;
