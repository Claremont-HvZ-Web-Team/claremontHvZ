$(function () {

    "use strict";

    $.getJSON(
        '/status/json/players.json',
        function(data, status, jqXHR) {
            console.log("successful stat GET");
            console.log(data);

            var class_holder = "#population_by_class";
            var school_holder = "#population_by_school";
            var dorm_holder = "#population_by_dorm";

            // var data = [
            //     {label: 'foo', data: [[1,300], [2,300], [3,300], [4,300], [5,300]]},
            //     {label: 'bar', data: [[1,800], [2,600], [3,400], [4,200], [5,0]]},
            //     {label: 'baz', data: [[1,100], [2,200], [3,300], [4,400], [5,500]]}
            // ];

            var class_options = {
                series: {stack: true,
                         lines: {show: false, steps: false },
                         bars: {show: true, barWidth: 0.9, align: 'center',},},
                xaxis: {
                    ticks: data.ticks.grad_year
                }
            };

            var school_options = {
                series: {stack: true,
                         lines: {show: false, steps: false },
                         bars: {show: true, barWidth: 0.9, align: 'center',},},
                xaxis: {
                    ticks: data.ticks.school
                }

            };

            var dorm_options = {
                series: {stack: true,
                         lines: {show: false, steps: false },
                         bars: {show: true, barWidth: 0.8, align: 'center', horizontal:true},},
                yaxis: {
                    ticks: data.ticks.dorm
                }
            };

            $.plot($(class_holder), data.grad_year, class_options);
            $.plot($(school_holder), data.school, school_options);
            $.plot($(dorm_holder), data.dorm, dorm_options);
        }
    );

    $('.noscript').remove();
    $('.scriptonly').show();
});
