const express = require("express");
const app = express();
const bodyParser = require("body-parser");

// Middleware for parsing JSON
app.use(bodyParser.json());

app.post("/predict", (req, res) => {
  const investors = req.body; // Expecting JSON array or object in the request body

  // Check if `investors` is empty or invalid
  if (!investors || (Array.isArray(investors) && investors.length === 0)) {
    return res.status(400).json({ error: "No stocks data provided." });
  }

  const recommendations = {
    message: "Successfully gave recommendations",
    data: investors,
  };

  res.status(200).json(recommendations); // Send the response
});

// Start the server
const port = 7000;
app.listen(port, () => {
  console.log(`AI service running on http://localhost:${port}`);
});
