(function ($) {
 "use strict";
 
	 /*----------------------------------------*/
	/*  1.  Basic Line Chart
	/*----------------------------------------*/
	var ctx = document.getElementById("basiclinechart");
	var basiclinechart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: label,
			datasets: [{
				label: "loss",
				fill: false,
                backgroundColor: '#00c292',
				borderColor: '#00c292',
				data: loss,
            }, {
                label: "val loss",
				fill: false,
                backgroundColor: '#fb9678',
				borderColor: '#fb9678',
				data: val_loss,
				
		}]
		},
		options: {
			responsive: true,
			title:{
				display:true,
				text:'Grafik Loss dan Val Loss'
			},
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'epoch'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Value'
					}
				}]
			}
		}
	});
	
	/*----------------------------------------*/
	/*  2.  Line Chart Interpolation
	/*----------------------------------------*/
	
	var ctx = document.getElementById("linechartinterpolation");
	var linechartinterpolation = new Chart(ctx, {
		type: 'line',
		data: {
			labels: label,
			datasets: [{
				label: "Accuracy",
				fill: false,
                backgroundColor: '#00c292',
				borderColor: '#00c292',
				data: accuracy,
				cubicInterpolationMode: 'monotone'
            }, {
                label: "Val Accuracy",
				fill: false,
                backgroundColor: '#fb9678',
				borderColor: '#fb9678',
				data: val_accuracy
				
		}]
		},
		options: {
			responsive: true,
			title:{
				display:true,
				text:'Grafik Accuracy dan Val Accuracy'
			},
			tooltips: {
				mode: 'index'
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Value'
					},
					ticks: {
						suggestedMin: 0,
						suggestedMax: 1,
					}
				}]
			}
		}
	});
	
	
	/*----------------------------------------*/
	/*  3.  Line Chart styles
	/*----------------------------------------*/
	
	var ctx = document.getElementById("linechartstyles");
	var linechartstyles = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["January", "February", "March"],
			datasets: [{
				label: "Unfilled",
				fill: false,
                backgroundColor: '#01c0c8',
				borderColor: '#01c0c8',
				data: [0, 15, 17, 200, 0, 12]
            }, {
                label: "Dashed",
				fill: false,
                backgroundColor: '#fb9678',
				borderColor: '#fb9678',
				borderDash: [5, 5],
				data: [-100, 200, 12, -200, 12]
				
		}]
		},
		options: {
			responsive: true,
			title:{
				display:true,
				text:'Line Chart Style'
			},
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Month'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Value'
					}
				}]
			}
		}
	});
	/*----------------------------------------*/
	/*  4.  Line Chart point circle
	/*----------------------------------------*/
	
	var ctx = document.getElementById("linechartpointcircle");
	var linechartpointcircle = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["May", "June", "July"],
			datasets: [{
				label: "My First dataset",
				backgroundColor: '#00c292',
				borderColor: '#00c292',
				data: [0, 10, 20, 30, 40, 50, 60],
				fill: false,
				pointRadius: 4,
				pointHoverRadius: 10,
				showLine: false 
			}]
		},
		options: {
			responsive: true,
			title:{
				display:true,
				text:'Line Chart Point Circle'
			},
			legend: {
				display: false
			},
			elements: {
				point: {
					pointStyle: 'circle',
				}
			}
		}
	});
	
	
		
})(jQuery); 