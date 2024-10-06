let hours, minutes, seconds, degrees, arcminutes, arcseconds;
let DEC, RA;
hours = 12;
minutes = 43;
seconds = 59.4;
degrees = -4;
arcminutes = 43;
arcseconds = 49.3;
DEC = degrees + arcminutes / 60 + arcseconds / 60;
RA = 15 * (hours + minutes / 60 + seconds / 60);

let aladin;
let overlay;
A.init.then(() => {
    aladin = A.aladin('#aladin-lite-div', { fov: 140, projection: "STG", cooFrame: 'equatorial', showCooGridControl: true, showSimbadPointerControl: true, showCooGrid: false });
    aladin.gotoRaDec(RA, DEC);
    var hips = A.catalogHiPS("/static/hips", {onClick: 'showTable', name: 'custom_sky'});  
    aladin.addCatalog(hips);
    overlay = A.graphicOverlay({color: '#FF0000', lineWidth: 2});
    aladin.addOverlay(overlay); // Add overlay once, it will be reused
});

function toggleMenu() {
    const upButton = document.getElementById("upButton");
    const downButton = document.getElementById("downButton");
    const menu = document.getElementById("menu");

    upButton.classList.toggle('hidden');
    downButton.classList.toggle('hidden');
    menu.classList.toggle('hidden');
}

// Path to your CSV file
const csvFilePath = "/static/planet_data.csv";

// Function to load and parse the CSV
async function loadCSV() {
    const response = await fetch(csvFilePath);
    const csvData = await response.text();

    // Use PapaParse to parse the CSV
    return Papa.parse(csvData, {
        header: false, // Assuming your CSV doesn't have a header
        skipEmptyLines: true // Skip empty lines
    }).data;
}

// Function to search for the term in the second column
async function searchCSV() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const csvData = await loadCSV();

    // Filter the data based on the second column (index 1)
    const results = csvData.filter(row => row[1].toLowerCase().includes(searchTerm));

    // Display the results
    displayResults(results);
}

// Function to display the results
function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No results found</p>';
        return;
    }

    // Create a table to display the results
    const table = document.createElement('table');
    results.forEach(row => {
        const rowElement = document.createElement('tr');
        /*row.slice(0, 2).forEach(cell => {
            const cellElement = document.createElement('td');
            cellElement.textContent = cell;
            rowElement.appendChild(cellElement);
        });*/

        const plName = row[0];
        const hostName = row[1];

        const plNameCell = document.createElement('td');
        plNameCell.textContent = plName;
        rowElement.appendChild(plNameCell);

        const hostNameCell = document.createElement('td');
        hostNameCell.textContent = hostName;
        rowElement.appendChild(hostNameCell);

        rowElement.onclick = () => {
            sendString(plName);
        };


        table.appendChild(rowElement);
    });

    resultsDiv.appendChild(table);
}

function sendString(inputString) {

    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputString: inputString }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Processed string from Python:', data.result);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
// Function to activate constellation drawing
let polylinePoints = [];  // Store the constellation points
function enableConstellationDrawing() {
    // Add event listener for mouse clicks (RA/Dec coordinates)
    aladin.on('click', function(coord) {
        let ra = coord.ra;   // Right Ascension (RA)
        let dec = coord.dec; // Declination (Dec)

        // Add clicked coordinates to polylinePoints
        polylinePoints.push([ra, dec]);

        console.log(`Added point: RA = ${ra}, Dec = ${dec}`);
    });

    // Add event listener for drawing the constellation
    /*document.getElementById('activate-constellation').addEventListener('click', function() {
        if (polylinePoints.length > 1) {  // You need at least two points to draw a line
            overlay.add(A.polyline(polylinePoints));  // Draw the polyline with the clicked points
            console.log("Constellation drawn:", polylinePoints);
        } else {
            console.log("Not enough points to draw a polyline.");
        }
    });*/
}

function activateConstellation(){
    
    if (polylinePoints.length > 1) {  // You need at least two points to draw a line
        overlay.add(A.polyline(polylinePoints));  // Draw the polyline with the clicked points
        console.log("Constellation drawn:", polylinePoints);
    } else {
        console.log("Not enough points to draw a polyline.");
    }
}
function deleteConstellation(){
    polylinePoints.length=0;
}
