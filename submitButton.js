const submitButton = document.querySelector('#submit');
const inputElement = document.querySelector('#exoplanet');
const outputElement = document.querySelector('#output');

submitButton.addEventListener('click', async () => {
    const exoplanetName = inputElement.value;

    try {
        const response = await fetch('http://localhost:3000/run-python', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain', // Sending as plain text
            },
            body: exoplanetName,  // Sending just the string directly
        });

        const data = await response.json();
        outputElement.textContent = data.output; // Display result from Python script
    } catch (error) {
        console.error('Error:', error);
    }
});
