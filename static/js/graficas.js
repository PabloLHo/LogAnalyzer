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

function graficaDispersion(id, nombre, visitas, tiempo, paginas){

    valor = [];

    var r = Math.random() * 255;
	var g = Math.random() * 255;
	var b = Math.random() * 255;

    for(var i = 0; i < tiempo.length; i++){
        valor.push({x:visitas[i],y:tiempo[i], label:'' + paginas[i]+ ''});
    }

	const data = {
		datasets: [{
			label: nombre,
			backgroundColor: 'rgb(' + r + ',' + g + ',' + b +')',
			borderColor: 'rgb(' + r + ',' + g + ',' + b +')',
			data: valor,
		}]
	};

	const config = {
	  type: 'scatter',
	  data: data,
	  options: {
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Visitas'
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Tiempo uso (min)'
                }
            }]
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              var datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
              var x = tooltipItem.xLabel;
              var y = tooltipItem.yLabel;
              var label = '';

              // Buscar el punto correspondiente a la posición del ratón
              for (var i = 0; i < data.datasets[tooltipItem.datasetIndex].data.length; i++) {
                var point = data.datasets[tooltipItem.datasetIndex].data[i];
                if (point.x == x && point.y == y) {
                  label = point.label;
                  break;
                }
              }

              // Devolver el nombre del punto
              return label;
            }
          }
        }
      }
	};

	const myChart = new Chart( document.getElementById(id),config);
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

function graficaBarrasTemporal(id, nombre, nombre2, visitas, fechas, tiempo){

	var r = Math.random() * 255;
	var g = Math.random() * 255;
	var b = Math.random() * 255;

	var r2 = Math.random() * 255;
	var g2 = Math.random() * 255;
	var b2 = Math.random() * 255;

    const data = {
		labels: fechas,
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
                },
                yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Visitas y Tiempo uso (h)'
                }
                }]
                }
	    },
	};
	const myChart = new Chart( document.getElementById(id),config);

}