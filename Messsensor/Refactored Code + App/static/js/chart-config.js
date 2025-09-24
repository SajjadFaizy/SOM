const chartConfig = {
    type: 'line',
    data: {
        labels: Array.from({length: 60}, (_, i) => i + 1),
        datasets: [{
            label: 'Temperature (°C)',
            data: [], // Changed from Array(60).fill(null) to empty array
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
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
};
