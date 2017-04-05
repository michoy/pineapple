
var genLectEx = genLectEx || (function(){
    return {
        genGraph : function(xObjects, classData) {
            const CHART = document.getElementById("lect_ex_chart");
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
                            pointBackgroundColor: "#ffa1dc",
                            pointBorderWidth: 1,
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "rgba(75,192,192,1)",
                            pointHoverBorderColor: "rgba(220,220,220,1)",
                            pointHoverBorderWidth: 2,
                            pointRadius: 1,
                            pointHitRadius: 10,
                            data: classData,
                            spanGaps: false,
                        },
                    ]
                }
            });
        }
    };
}());

var genLectTag = genLectTag || (function(){
    return {
        genGraph : function(xObjects, classData) {
            const CHART = document.getElementById("lect_tag_chart");
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
                            data: classData,
                            spanGaps: false,
                        },
                    ]
                }
            });
        }
    };
}());




var genCardPie = genCardPie || (function(){
    return {
        genGraph : function(targetId, success) {
            const CHART = document.getElementById(targetId);
            console.log(CHART);
            var pieChart = new Chart(CHART, {
                type: 'pie',
                data: {
                    labels: ['Correct', 'Incorrect'],
                    datasets: [
                        {
                            backgroundColor: ["#ffbb33","#00C851"],
                            boarderWidth: 1,
                            fillColor : ["#007E33","#007E33"],
                            strokeColor : ["#007E33","#007E33"],
                            pointColor : ["#007E33","#007E33"],
                            pointStrokeColor : "#007E33",
                            data : [success, 100-success]
                        },
                    ]
                }
            });
        }
    };
}());


