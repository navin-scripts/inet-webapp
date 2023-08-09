const doc = document

// Step 1: Create an object to store the data
var dataObj = {};
console.log(trafficData)
const sumReduced = trafficData.reduce((accumulator, currentValue) => accumulator + currentValue.recv, 0);
const convertedNumber = (sumReduced / 1000000).toFixed(2);
console.log(sumReduced)
// Update the <h2> element with the calculated sum in GB
const networkSumElement = document.getElementById('networkSum');
networkSumElement.textContent = convertedNumber + ' GB';


trafficData.sort(function(a, b) {
  return b.recv - a.recv;
});

// console.log(trafficData);

var top5 = trafficData.slice(0, 4);

// Step 2: Iterate over trafficData and update the data object
for (var i = 0; i < top5.length; i++) {
    var entry = trafficData[i];
    var application = entry.application;
    var recv = entry.recv;

    if (dataObj[application]) {
      // If it exists, add the recv value to the existing value
      dataObj[application] += recv;
    } else {
      // If it doesn't exist, initialize the value with recv
      dataObj[application] = recv;
    }
}
// Step 3: Generate labels and series arrays based on the data object
var labels = Object.keys(dataObj);
var series = Object.values(dataObj);

if (doc.querySelector('.traffic')) {
    new Chartist.Line('.traffic', {
        labels: labels,
        series: [
            series
        ]
    }, {
        // low: 0,
        showArea: true,
        fullWidth: false,
        plugins: [
        ],
        axisX: {
            // On the x-axis start means top and end means bottom
            position: 'end',
            showGrid: false
        },
        axisY: {
            // On the y-axis start means left and end means right
            // showGrid: true,
            showLabel: true,
            labelInterpolationFnc: function (value) {
                // Convert KB to GB
                var gbValue = value / 1024 / 1024;
                return gbValue.toFixed(2) + ' GB';
            }
        }
    });
}
