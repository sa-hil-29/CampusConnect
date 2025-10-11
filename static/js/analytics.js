// CampusConnect Analytics JS - Chart Interactions (Separate File)
document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('placementsChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        
        // Fetch data from Django endpoint
        fetch('/dashboard/data/')  // URL to analytics_data view
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                return response.json();
            })
            .then(chartData => {
                const chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: chartData.labels || [],
                        datasets: [{
                            label: 'Selected Placements by Branch',
                            data: chartData.data || [],
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top' },
                            title: { display: true, text: 'Placements by Branch' }
                        },
                        scales: {
                            y: { beginAtZero: true }
                        },
                        onClick: function(event, elements) {
                            if (elements.length > 0) {
                                const index = elements[0].index;
                                const branch = chartData.labels[index];
                                const count = chartData.data[index];
                                alert(`Branch: ${branch} - Placements: ${count}`);
                            }
                        }
                    }
                });
                
                // Export button
                const exportBtn = document.getElementById('export-chart');
                if (exportBtn) {
                    exportBtn.addEventListener('click', function() {
                        const link = document.createElement('a');
                        link.download = 'placements.png';
                        link.href = canvas.toDataURL('image/png');
                        link.click();
                    });
                }
            })
            .catch(error => {
                console.error('Chart error:', error);
                ctx.fillText('Error loading chart data', canvas.width / 2, canvas.height / 2);
            });
    }
});