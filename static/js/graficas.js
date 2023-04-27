//Tipos:
// Barra - bar
// Lineas - line
// Burbujas - bubble
// Circular - doughnut
// Dispersion - scatter

//Mas info - https://www.chartjs.org/docs/latest/samples/information.html

function graficaBarras(id, nombre, visitas, paginas){

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
	  type: 'bar',
	  data: data,
	  options: {
	    legend: {
            display: false
        },
	  },
	};

	const myChart = new Chart( document.getElementById(id),config);
	myChart.canvas.parentNode.style.width = '100%';
	myChart.canvas.parentNode.style.heigth = '100%';

}

function graficaCircular(id, nombre, visitas, paginas){
    colores = [];
    for(var i = 0; i < visitas.length; i++){
    	var r = Math.random() * 255;
        var g = Math.random() * 255;
        var b = Math.random() * 255;
        colores.push('rgb(' + r + ',' + g + ',' + b +')');
    }
    const data = {
      labels: paginas,
      datasets: [
        {
          label: 'Visitas por página',
          data: visitas,
          backgroundColor: colores,
        }
      ]
    };

    const config = {
      type: 'doughnut',
      data: data,
      options: {
        responsive: true,
        legend: {
            display: false
        }
      },
    };

    const myChart = new Chart( document.getElementById(id),config);
	myChart.canvas.parentNode.style.width = '100%';
}

function graficaMixta(id, nombre,nombre2, visitas, paginas, tiempo){
    var r = Math.random() * 255;
	var g = Math.random() * 255;
	var b = Math.random() * 255;
	var r2 = Math.random() * 255;
	var g2 = Math.random() * 255;
	var b2 = Math.random() * 255;
	const data = {
		labels: paginas,
		datasets: [{
			label: nombre,
			backgroundColor: 'rgb(' + r + ',' + g + ',' + b +')',
			borderColor: 'rgb(' + r + ',' + g + ',' + b +')',
			data: visitas,
			order: 1,
		},
		{
		    label: nombre2,
		    data: tiempo,
			borderColor: 'rgb(' + r2 + ',' + g2 + ',' + b2 +')',
			type: 'line',
			order: 0,
		}]
	};

	const config = {
	  type: 'bar',
	  data: data,
	    options: {
    scales: {
      xAxes: [{
        ticks: {
          display: false,
        }
      }],
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Visitas (Barra) y Minutos de uso (Linea)'
        }
      }]
    }
  }
	};

	const myChart = new Chart( document.getElementById(id),config);
}