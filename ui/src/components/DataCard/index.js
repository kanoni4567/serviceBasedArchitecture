import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { Typography, Card, CardContent } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles({
  root: {
    minWidth: 275,
    maxWidth: 500
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)"
  },
  title: {
    fontSize: 12
  },
  pos: {
    marginBottom: 12
  }
});

export default function DataCard() {
  const classes = useStyles();
  const [data, setData] = useState({});

  const getData = () => {
    Promise.all([
      axios.get("http://localhost:8100/events/stats"),
      axios.get("http://localhost:8110/items?offset=1"),
      axios.get("http://localhost:8110/wishlistItems?offset=1")
    ]).then(arr => {
      console.log("arr", arr);
      setData({
        numItemPostings: arr[0].data["num_item_postings"],
        numWishlistItems: arr[0].data["num_wishlist_items"],
        updatedTimestamp: arr[0].data["updated_timestamp"],
        firstItemPosting: arr[1].data,
        firstWishlistItem: arr[2].data
      });
    });
  };

  useEffect(() => {
      setTimeout(getData, 2000);
  }, [data]);

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          Number of Item Posts
        </Typography>
        <Typography  component="h5" >
          {data.numItemPostings}
        </Typography>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          Number of Wishlist Items
        </Typography>
        <Typography  component="h5" >
          {data.numWishlistItems}
        </Typography>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          First Item Name
        </Typography>
        <Typography  component="h5" >
          {data.firstItemPosting && data.firstItemPosting.name}
        </Typography>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          First Wishlist Item ID
        </Typography>
        <Typography  component="h5" >
          {data.firstWishlistItem && data.firstWishlistItem['itemId']}
        </Typography>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          Last Updated
        </Typography>
        <Typography  component="h5" >
          {data.updatedTimestamp}
        </Typography>
      </CardContent>
    </Card>
  );
}
