// Asign a 2D-Graph interface to the HTML element <canvas>
const ctx = document.getElementById('temperatureChart').getContext('2d');

// Create chart (from chart.js lib) and pass ctx, so it knows where to draw it
const chart = new Chart(ctx, {

    type: 'line', // line, bar, pie, doughnut, radar, scatter, bubble

    data: {
        labels: Array.from({length: 60}, (_, i) => i + 1), // X-axis from 1 to 60ºC
        datasets: [{
            label: 'Temperature (°C)', // Leyend
            data: [], // Init empty, dinamically filled
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false // Whether area below line colored
        }]
    },

    options: {
        responsive: true, // Graph dinamically adapts to container width
        scales: {
            x: {
                title: { display: true, text: 'Time (Latest 60 Samples)' }
            },
            y: {
                title: { display: true, text: 'Temperature (°C)' }
            }
        }
    }
});

const devMode = false; // Set to true to use mock data --> serves to only test the graph without the server
async function fetchData() {
    if (devMode === true) {
        const lastDataPoint = chart.data.datasets[0].data.slice(-1)[0] || 25; // Default to 25 if no data
        const newDataPoint = parseFloat((lastDataPoint + (Math.random() * 4 - 2)).toFixed(2));
    
        console.log("New data point:", newDataPoint);
    
        if (chart.data.datasets[0].data.length >= 60) {
            chart.data.datasets[0].data.shift(); // Remove the oldest data point
        }
    
        chart.data.datasets[0].data.push(newDataPoint); // Add the new data point
        chart.update();
    } else {
        const response = await fetch('/data'); // Response Type Object
        const data = await response.json(); // Convert Response body to JSON

        console.log("Aquí va data:", data)

        if (data.length > 0) {  // Verifies it's not empty
            chart.data.datasets[0].data = data;
            chart.update();
        } else {
            console.error("No hay datos disponibles");
        }
    }
}

// fetchData will execute automatically every second (1000ms) indefinitely
setInterval(fetchData, 1000);