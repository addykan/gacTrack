import React from "react";
import { Card, Typography, Grid } from "@material-ui/core";

function AssignmentCard({ assignment }) {
  return (
    <Grid item xs={4}>
      <Card style={{ borderRadius: 20 }}>
        <Grid container alignItems="center" justify="center" spacing={1}>
          <Grid item xs={7}>
            <Typography>{assignment.name}</Typography>
          </Grid>
          <Grid item xs={5}>
            <Typography>{assignment.class}</Typography>
          </Grid>
          <Grid item xs={7}>
            <Typography>{assignment.dueDate}</Typography>
          </Grid>
          <Grid item xs={5}>
            <Typography>{assignment.status}</Typography>
          </Grid>
        </Grid>
      </Card>
    </Grid>
  );
}

export default AssignmentCard;
