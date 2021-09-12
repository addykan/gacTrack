import React, { useState, useEffect } from "react";
import { Typography, TextField, FormGroup } from "@material-ui/core";

function Time() {
  const [hours, setHours] = useState(new Date().getHours());
  const [minutes, setMinutes] = useState(new Date().getMinutes());
  const [name, setName] = useState(localStorage.getItem("name"));
  const [nameText, setNameText] = useState("");
  useEffect(() => {
    const refreshClock = () => {
      let hours = new Date().getHours();
      let mins = new Date().getMinutes();
      setHours(hours < 10 ? "0" + hours : hours);
      setMinutes(mins < 10 ? "0" + mins : mins);
    };
    refreshClock();
    const timerId = setInterval(refreshClock, 1000);
  }, []);

  const handleNameSave = (e) => {
    e.preventDefault();
    setName(nameText);
    localStorage.setItem("name", nameText);
  };
  const clearName = (e) => {
    setName(null);
    localStorage.removeItem("name");
  };
  return (
    <>
      <Typography
        style={{ color: "white", fontWeight: "normal", fontSize: "10em" }}
        variant="h1"
      >
        {hours}:{minutes}
      </Typography>
      <Typography
        style={{ color: "white", fontWeight: "normal", fontSize: "4em" }}
        variant="h1"
        onClick={clearName}
      >
        {name !== null
          ? hours < 12
            ? "Good Morning "
            : hours < 4
            ? "Good Afternoon "
            : "Good Evening "
          : "What's your name?"}
        {name !== null ? (
          name
        ) : (
          <form onSubmit={handleNameSave}>
            <TextField
              onChange={(e) => setNameText(e.target.value)}
              value={name}
              style={{ width: "20vw", borderColor: "white" }}
              color="white"
              autoFocus
              inputProps={{
                style: {
                  color: "white",
                  fontWeight: "normal",
                  fontSize: "3em",
                  textAlign: "center",
                },
              }} // font size of input text
            />
          </form>
        )}
      </Typography>
    </>
  );
}

export default Time;
