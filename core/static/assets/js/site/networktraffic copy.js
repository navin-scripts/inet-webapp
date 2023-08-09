const doc = document

// Step 1: Create an object to store the data
var dataObj = {};

// Step 2: Iterate over trafficData and update the data object
for (var i = 0; i < trafficData.length; i++) {
    var entry = trafficData[i];
    var application = entry.application;
    var recv = entry.recv;
  
    // Check if the application is Facebook, YouTube, Instagram, or Snapchat
    if (application === 'Facebook' || application === 'iTunes' || application === 'Microsoft Teams') {
      // Check if the application already exists in the data object
      if (dataObj[application]) {
        // If it exists, add the recv value to the existing value
        dataObj[application] += recv;
      } else {
        // If it doesn't exist, initialize the value with recv
        dataObj[application] = recv;
      }
      console.log(dataObj[application]);
    } 
    // else if (application === '') {
        
    // }
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
        // showArea: true,
        // fullWidth: true,
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
