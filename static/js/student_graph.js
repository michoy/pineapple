
var genStudEx = genStudEx || (function(){
    return {
        genGraph : function(xObjects, classData, studData) {
            const CHART = document.getElementById("stud_ex_chart");
            console.log(CHART);
            var lineChart = new Chart(CHART, {
                type: 'line',
                data: {
                    labels: xObjects,
                    datasets: [
                        {
                            label: "Class performance %",
                            fill: false,
                            lineTension: 0.1,
                            backgroundColor: "rgba(255,117,0,0.4)",
                            borderColor: "rgba(255,117,0,1)",
                            borderCapStyle: 'butt',
                            borderDash: [],
                            borderDashOffset: 0.0,
                            borderJoinStyle: 'miter',
                            pointBorderColor: "rgba(255,117,0,1)",
                            pointBackgroundColor: "#fff",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            data: studData,
                            spanGaps: false,
                        },
                        {
                            label: "Your performance %",
                            fill: false,
                            lineTension: 0.1,
                            backgroundColor: "rgba(75,192,192,0.4)",
                            borderColor: "rgba(75,192,192,1)",
                            borderCapStyle: 'butt',
                            borderDash: [],
                            borderDashOffset: 0.0,
                            borderJoinStyle: 'miter',
                            pointBorderColor: "rgba(75,192,192,1)",
                            pointBackgroundColor: "#fff",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            data: classData,
                            spanGaps: false,
                        }
                    ]
                }
            });
        }
    };
}());

var genStudTag = genStudTag || (function(){
    return {
        genGraph : function(xObjects, classData, studData) {
            const CHART = document.getElementById("stud_tag_chart");
            console.log(CHART);
            var lineChart = new Chart(CHART, {
                type: 'line',
                data: {
                    labels: xObjects,
                    datasets: [
                        {
                            label: "Class performance %",
                            fill: false,
                            lineTension: 0.1,
                            backgroundColor: "rgba(255,117,0,0.4)",
                            borderColor: "rgba(255,117,0,1)",
                            borderCapStyle: 'butt',
                            borderDash: [],
                            borderDashOffset: 0.0,
                            borderJoinStyle: 'miter',
                            pointBorderColor: "rgba(255,117,0,1)",
                            pointBackgroundColor: "#fff",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            data: studData,
                            spanGaps: false,
                        },
                        {
                            label: "Your performance %",
                            fill: false,
                            lineTension: 0.1,
                            backgroundColor: "rgba(75,192,192,0.4)",
                            borderColor: "rgba(75,192,192,1)",
                            borderCapStyle: 'butt',
                            borderDash: [],
                            borderDashOffset: 0.0,
                            borderJoinStyle: 'miter',
                            pointBorderColor: "rgba(75,192,192,1)",
                            pointBackgroundColor: "#fff",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            data: classData,
                            spanGaps: false,
                        }
                    ]
                }
            });
        }
    };
}());