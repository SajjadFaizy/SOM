class TemperatureDataService {
    async fetchTemperatureData() {
        try {
            const response = await fetch('/data');
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }
}