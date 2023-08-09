"use strict";
const labels = trafficData.map(entry => entry.application);
const recvData = trafficData.map(entry => entry.recv);

console.log(labels);

const colors = Array.from({length: trafficData.length}, () => randomColor());

const ctx = document.getElementById('nettraffic').getContext('2d');

new Chartist.pie(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: recvData,
        backgroundColor: colors,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: 'right',
      },
    }
  });

  function randomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

