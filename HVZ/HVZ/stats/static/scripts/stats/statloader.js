$(function () {

    $.getJSON(
        '/stats/json/players',
        function(data, status, jqXHR) {
            abort = false;
            console.log("successful stat GET");
            console.log(data);

            var css_id = "#population_by_class";

            // var data = [
            //     {label: 'foo', data: [[1,300], [2,300], [3,300], [4,300], [5,300]]},
            //     {label: 'bar', data: [[1,800], [2,600], [3,400], [4,200], [5,0]]},
            //     {label: 'baz', data: [[1,100], [2,200], [3,300], [4,400], [5,500]]}
            // ];

            var options = {
                series: {stack: 0,
                         lines: {show: false, steps: false },
                         bars: {show: true, barWidth: 0.9, align: 'center',},},
                xaxis: {ticks: [[1,'One'], [2,'Two'], [3,'Three'], [4,'Four'], [5,'Five']]},
            };

            $.plot($(css_id), data, options);
        }
    );
});
