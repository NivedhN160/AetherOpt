let energyChartInstance = null;

function renderEnergyChart(canvasId, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    if (energyChartInstance) {
        energyChartInstance.destroy();
    }
    
    // Normalize data length to maximum steps
    let maxLen = 0;
    datasets.forEach(ds => {
        if (ds.data && ds.data.length > maxLen) {
            maxLen = ds.data.length;
        }
    });
    
    const labels = Array.from({length: maxLen}, (_, i) => i);
    
    // Assign colors
    const colors = ['#38bdf8', '#34d399', '#fbbf24', '#f87171', '#c084fc', '#a3e635'];
    
    const chartDatasets = datasets.map((ds, i) => {
        return {
            label: ds.label,
            data: ds.data,
            borderColor: colors[i % colors.length],
            borderWidth: 2,
            tension: 0.1,
            pointRadius: 0
        };
    });

    energyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: chartDatasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)'
                }
            },
            scales: {
                x: {
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Steps', color: '#cbd5e1' }
                },
                y: {
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Energy', color: '#cbd5e1' }
                }
            }
        }
    });
}

window.renderEnergyChart = renderEnergyChart;
