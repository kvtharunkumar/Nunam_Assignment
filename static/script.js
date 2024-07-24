// document.addEventListener("DOMContentLoaded", function () {
//   // Fetch State of Health Data
//   fetch("/api/soh")
//     .then((response) => response.json())
//     .then((data) => {
//       createPieChart("pieChart", data);
//     });

//   // Fetch Cell Data
//   fetch("/api/cell_data/5308")
//     .then((response) => response.json())
//     .then((data) => {
//       createLineChart("lineChart", data);
//     });
// });

// function createPieChart(canvasId, data) {
//   const ctx = document.getElementById(canvasId).getContext("2d");
//   new Chart(ctx, {
//     type: "pie",
//     data: {
//       labels: data.map((item) => item.cell_id),
//       datasets: [
//         {
//           data: data.map((item) => item.soh),
//           backgroundColor: ["#ff6384", "#36a2eb"], // Adjust colors as needed
//         },
//       ],
//     },
//   });
// }

// function createLineChart(canvasId, data) {
//   const ctx = document.getElementById(canvasId).getContext("2d");
//   new Chart(ctx, {
//     type: "line",
//     data: {
//       labels: data.map((item) => item.time),
//       datasets: [
//         {
//           label: "Current Data",
//           data: data.map((item) => item.current),
//           borderColor: "#ff6384",
//           fill: false,
//         },
//         {
//           label: "Voltage Data",
//           data: data.map((item) => item.voltage),
//           borderColor: "#36a2eb",
//           fill: false,
//         },
//       ],
//     },
//   });
// }
