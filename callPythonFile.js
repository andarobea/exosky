const express = require('express');
const { spawn } = require('child_process');
const app = express();

// Parse JSON bodies (as sent by API clients)
app.use(express.json());

// Endpoint to call the Python script
app.post('/compute', (req, res) => {
    const exoplanetName = req.body.exoplanetName;  // Get the exoplanet name from the request body

    // Spawn a new Python process to run the Python script
    const python = spawn('python', ['./handle_request.py', exoplanetName]);

    // Collect data from Python script
    python.stdout.on('data', (data) => {
        console.log(`Data from Python script: ${data}`);
        res.send(data.toString());  // Send the output back to the client
    });

    // Error handling
    python.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
        res.status(500).send('Error occurred while running the Python script');
    });

    // When the Python script ends
    python.on('close', (code) => {
        console.log(`Python script finished with code ${code}`);
    });
});

// Start the server on port 3000
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
