//Tipos:
// Barra - bar
// Lineas - line
// Burbujas - bubble
// Circular - doughnut
// Dispersion - scatter

//Mas info - https://www.chartjs.org/docs/latest/samples/information.html

function calculoGrafica(tipo, id, nombre, paginas, visitas){

	var r = Math.random() * 255;
	var g = Math.random() * 255;
	var b = Math.random() * 255;
	const data = {
		labels: paginas,
		datasets: [{
			label: nombre,
			backgroundColor: 'rgb(' + r + ',' + g + ',' + b +')',
			borderColor: 'rgb(' + r + ',' + g + ',' + b +')',
			data: visitas,
		}]
	};

	const config = {
	  type: tipo,
	  data: data,
	  options: {
		// maintainAspectRatio : true,
		scales: {
		  x: {
			title: {
			  display: true,
			  text: 'Páginas'
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
			  text: 'Visitas'
			}
		  }
		}
	  },
	};

	const myChart = new Chart( document.getElementById(id),config);
	myChart.canvas.parentNode.style.width = '100%';

}