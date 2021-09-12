import React, { useState, useEffect } from "react";
import { Typography } from "@material-ui/core";

function Time() {
  const [hours, setHours] = useState(new Date().getHours());
  const [minutes, setMinutes] = useState(new Date().getMinutes());

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

  return (
    <Typography
      style={{ color: "white", fontWeight: "normal", fontSize: "10em" }}
      variant="h1"
    >
      {hours}:{minutes}
    </Typography>
  );
}

export default Time;
