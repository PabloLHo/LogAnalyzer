//Tipos:
// Barra - bar
// Lineas - line
// Burbujas - bubble
// Circular - doughnut
// Dispersion - scatter

//Mas info - https://www.chartjs.org/docs/latest/samples/information.html

function calculoGrafica(tipo, id, nombre ,tiempo){
	const labels = [new Date('2022-09-01T00:00:00'), new Date('2022-09-02T00:00:00'), new Date('2022-09-03T00:00:00'), new Date('2022-09-04T00:00:00'), new Date('2022-09-05T00:00:00'), new Date('2022-09-06T00:00:00'), new Date('2022-09-07T00:00:00'),
	new Date('2022-09-08T00:00:00'), new Date('2022-09-09T00:00:00'), new Date('2022-09-10T00:00:00'), new Date('2022-09-11T00:00:00'), new Date('2022-09-12T00:00:00'), new Date('2022-09-13T00:00:00'), new Date('2022-09-14T00:00:00'),
	new Date('2022-09-15T00:00:00'), new Date('2022-09-16T00:00:00'), new Date('2022-09-17T00:00:00'), new Date('2022-09-18T00:00:00'), new Date('2022-09-19T00:00:00'), new Date('2022-09-20T00:00:00'), new Date('2022-09-21T00:00:00'),
	new Date('2022-09-22T00:00:00'), new Date('2022-09-23T00:00:00'), new Date('2022-09-24T00:00:00'), new Date('2022-09-25T00:00:00'), new Date('2022-09-26T00:00:00'), new Date('2022-09-27T00:00:00'), new Date('2022-09-28T00:00:00'),
	new Date('2022-09-29T00:00:00'), new Date('2022-09-30T00:00:00'), new Date('2022-10-01T00:00:00'), new Date('2022-10-02T00:00:00'), new Date('2022-10-03T00:00:00'), new Date('2022-10-04T00:00:00'), new Date('2022-10-05T00:00:00'), new Date('2022-10-06T00:00:00'), new Date('2022-10-07T00:00:00'),
	new Date('2022-10-08T00:00:00'), new Date('2022-10-09T00:00:00'), new Date('2022-10-10T00:00:00'), new Date('2022-10-11T00:00:00'), new Date('2022-10-12T00:00:00'), new Date('2022-10-13T00:00:00'), new Date('2022-10-14T00:00:00'),
	new Date('2022-10-15T00:00:00'), new Date('2022-10-16T00:00:00'), new Date('2022-10-17T00:00:00'), new Date('2022-10-18T00:00:00'), new Date('2022-10-19T00:00:00'), new Date('2022-10-20T00:00:00'), new Date('2022-10-21T00:00:00'),
	new Date('2022-10-22T00:00:00'), new Date('2022-10-23T00:00:00'), new Date('2022-10-24T00:00:00'), new Date('2022-10-25T00:00:00'), new Date('2022-10-26T00:00:00'), new Date('2022-10-27T00:00:00'), new Date('2022-10-28T00:00:00'),
	new Date('2022-10-29T00:00:00'), new Date('2022-10-30T00:00:00'), new Date('2022-10-31T00:00:00'), new Date('2022-11-01T00:00:00'), new Date('2022-11-02T00:00:00'), new Date('2022-11-03T00:00:00'), new Date('2022-11-04T00:00:00'), new Date('2022-11-05T00:00:00'), new Date('2022-11-06T00:00:00'), new Date('2022-11-07T00:00:00'),
	new Date('2022-11-08T00:00:00'), new Date('2022-11-09T00:00:00'), new Date('2022-11-10T00:00:00'), new Date('2022-11-11T00:00:00'), new Date('2022-11-12T00:00:00'), new Date('2022-11-13T00:00:00'), new Date('2022-11-14T00:00:00'),
	new Date('2022-11-15T00:00:00'), new Date('2022-11-16T00:00:00'), new Date('2022-11-17T00:00:00'), new Date('2022-11-18T00:00:00'), new Date('2022-11-19T00:00:00'), new Date('2022-11-20T00:00:00'), new Date('2022-11-21T00:00:00'),
	new Date('2022-11-22T00:00:00'), new Date('2022-11-23T00:00:00'), new Date('2022-11-24T00:00:00'), new Date('2022-11-25T00:00:00'), new Date('2022-11-26T00:00:00'), new Date('2022-11-27T00:00:00'), new Date('2022-11-28T00:00:00'),
	new Date('2022-11-29T00:00:00'), new Date('2022-11-30T00:00:00')];
	const data2 = [];

	for (let i = 0; i < 91; ++i) {
		data2.push(Math.random() * 20);
	}
	var r = Math.random() * 255;
	var g = Math.random() * 255;
	var b = Math.random() * 255;
	const data = {
		labels: labels,
		datasets: [{
			label: nombre,
			backgroundColor: 'rgb(' + r + ',' + g + ',' + b +')',
			borderColor: 'rgb(' + r + ',' + g + ',' + b +')',
			data: data2,
		}]
	};

	const config = {
	  type: tipo,
	  data: data,
	  options: {
		// maintainAspectRatio : true,
		scales: {
		  x: {
			type: "time",
			title: {
			  display: true,
			  text: 'Fecha recogida de datos'
			},
			time: {
				unit: tiempo,
				isoWeekday: true,
				stepSize: 1
			},
			grid: {
				color: 'rgb(0,0,0)'
			},
			ticks: {
				display: true,
				source: 'auto'
			}
		  },
		  y: {
			title: {
			  display: true,
			  text: 'Kg / m2'
			}
		  }
		}
	  },
	};

	const myChart = new Chart( document.getElementById(id),config);
	myChart.canvas.parentNode.style.width = '100%';

}
