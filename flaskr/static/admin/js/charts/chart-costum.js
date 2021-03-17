(function ($) {
 "use strict";

	/*----------------------------------------*/
	/*--------------GROUP BAR-----------------*/
	/*----------------------------------------*/
	var ctx = document.getElementById("groupbar");
	var groupbar = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10"],
		    datasets: [{
				label: "Accuracy",
                backgroundColor: "#81c7a7",
                borderColor: "#3c8c40",
                borderWidth: 1,
                data: accuracy
			},
            {
              label: "Precision",
              backgroundColor: "#f77b72",
              borderColor: "#f44336",
              borderWidth: 1,
              data: presisi
            },
            {
              label: "F1-Score",
              backgroundColor: "#79c0f7",
              borderColor: "#135a91",
              borderWidth: 1,
              data: f1
            },
            {
              label: "Recall",
              backgroundColor: "#bd72f7",
              borderColor: "#844fac",
              borderWidth: 1,
              data: recall
            }]
		},
		options: {
			  responsive: true,
              legend: {
                position: "top"
              },
              title: {
                display: true,
                text: "RESULT K-FOLD CROSS VALIDATION"
              },
              scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: true
                  }
                }]
              }
		}
	});
})(jQuery);