const ctx = document.getElementById('temperatureChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array.from({length: 60}, (_, i) => i + 1),
        datasets: [{
            label: 'Temperature (°C)',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
        animation: false,
        responsive: true,
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


async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    
    if (data.length > 0) {
        chart.data.datasets[0].data = data.map(item => item.temp);
        chart.update();
    }
}

setInterval(fetchData, 1000);
