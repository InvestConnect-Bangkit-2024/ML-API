const express = require("express");
const app = express();
const bodyParser = require("body-parser");
require("dotenv").config();

app.use(bodyParser.json());

app.post("/predict", (req, res) => {
  const investors = req.body;

  if (!investors || (Array.isArray(investors) && investors.length === 0)) {
    return res.status(400).json({ error: "No stocks data provided." });
  }

  const recommendations = {
    message: "Successfully gave recommendations",
    data: investors,
  };

  res.status(200).json(recommendations);
});

const port = process.env.PORT;
app.listen(port, () => {
  console.log(`AI service running on port:${port}`);
});
