(function ($) {
 "use strict";
	 /*----------------------------------------*/
	/*  1.  Bar Chart
	/*----------------------------------------*/

	var ctx = document.getElementById("barchart1");
	var barchart1 = new Chart(ctx, {
		type: type,
		data: {
			labels: ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10"],
			datasets: [{
				label: 'Accuracy K-Fold',
				data: accuracy,
				backgroundColor: 'rgba(255, 99, 132, 0.2)',
				borderColor: 'rgba(255,99,132,1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});
	/*----------------------------------------*/
	/*  2.  Bar Chart vertical
	/*----------------------------------------*/
	var ctx = document.getElementById("barchart2");
	var barchart2 = new Chart(ctx, {
		type: type,
		data: {
			labels: ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10"],
			datasets: [{
				label: 'Presisi K-Fold',
				data: presisi,
				backgroundColor: 'rgb(50,205,50, 0.2)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});
	
	/*----------------------------------------*/
	/*  3.  Bar Chart Horizontal
	/*----------------------------------------*/
	var ctx = document.getElementById("barchart3");
	var barchart3 = new Chart(ctx, {
		type: type,
		data: {
			labels: ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10"],
			datasets: [{
				label: 'Recall K-Fold',
				data: recall,
				backgroundColor:'rgba(255, 206, 86, 0.2)',
				borderColor:'rgba(255, 206, 86, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});
	
	/*----------------------------------------*/
	/*  4.  Bar Chart Multi axis
	/*----------------------------------------*/
	var ctx = document.getElementById("barchart4");
	var barchart4 = new Chart(ctx, {
		type: type,
		data: {
			labels: ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10"],
			datasets: [{
				label: 'F1-Score K-Fold',
				data: f1,
				backgroundColor:'rgba(75, 192, 192, 0.2)',
				borderColor:'rgba(75, 192, 192, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			}
		}
	});
	
	
		
})(jQuery); 