const express = require('express');
const { spawn } = require('child_process');
const app = express();
const cors = require('cors');
const port = 3000;

// Middleware to handle plain text (when the client sends a plain string)
app.use(express.text());

app.use(cors());

app.post('/run-python', (req, res) => {
    const exoplanetName = req.body;  // In this case, req.body will be the plain string sent by the client

    console.log(`Received exoplanetName: ${exoplanetName}`);

    // Use the received string as an argument for the Python script
    const pythonProcess = spawn('python', ['./handle_request.py', exoplanetName]);

    let output = '';
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.on('close', (code) => {
        res.json({ output });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data.toString()}`);  // Ensure errors are properly logged
    });
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
