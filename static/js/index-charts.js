<script>
window.chartColors = {
    green: '#75c181',
    gray: '#a9b5c9',
};

// Fetch data function with alert for debugging
function fetchBillData(url) {
    alert('fetchBillData called');  // Debugging: Check if this function is being called
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched Data:', data);  // Debugging: Check if data is being received
            return data;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error fetching data: ' + error);  // Show any error
        });
}

function createLineChart(data) {
    alert('Creating Line Chart');  // Debugging: Check if chart creation function is called
    var ctx = document.getElementById('canvas-linechart1').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Total Bills',
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    data: data.total_bills,
                    fill: false,
                },
                {
                    label: 'Paid Bills',
                    backgroundColor: window.chartColors.gray,
                    borderColor: window.chartColors.gray,
                    data: data.paid_bills,
                    fill: false,
                }
            ]
        }
    });
}

function createBarChart(data) {
    alert('Creating Bar Chart');  // Debugging: Check if bar chart creation is called
    var ctx = document.getElementById('canvas-barchart1').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Paid Bills',
                    backgroundColor: window.chartColors.green,
                    data: data.paid_bills,
                },
                {
                    label: 'Unpaid Bills',
                    backgroundColor: window.chartColors.gray,
                    data: data.unpaid_bills,
                }
            ]
        }
    });
}

window.addEventListener('load', function() {
    alert('Page Loaded');  // Debugging: Check if page load event is triggered

    // Fetch data for the line chart
    fetchBillData("{% url 'SDO:bills_per_month' %}").then(data => {
        createLineChart(data);
    });

    // Fetch data for the bar chart
    fetchBillData("{% url 'SDO:bills_per_year' %}").then(data => {
        createBarChart(data);
    });
});
</script>

<!-- Canvas elements to display the charts -->
<canvas id="canvas-linechart1"></canvas>
<canvas id="canvas-barchart1"></canvas>
