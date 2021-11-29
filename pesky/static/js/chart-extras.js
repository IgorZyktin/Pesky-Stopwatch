const OPTIONS = {
    scales: {
        y: {
            stacked: false,
            beginAtZero: true,
            min: 0
        },
        x: {
            stacked: false
        }
    }
}


function updateChart(chart, start, stop) {
    // Перерисовать график с нужными датами
    let xhr = new XMLHttpRequest();

    xhr.open("GET", `/api/chartjs/${start}/${stop}`, true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                chart.data = JSON.parse(xhr.responseText);
                chart.update()
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };
    xhr.send(null);
}
