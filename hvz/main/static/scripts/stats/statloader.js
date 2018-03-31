$(function() {
    "use strict";

    var class_holder = "#population_by_class";
    var school_holder = "#population_by_school";
    var dorm_holder = "#population_by_dorm";

    var json_data, class_options, school_options, dorm_options;

    function renderStats() {
        $.plot($(class_holder), json_data.grad_year, class_options);
        $.plot($(school_holder), json_data.school_id, school_options);
        $.plot($(dorm_holder), json_data.dorm_id, dorm_options);
    }

    $('.noscript').remove();
    $('.scriptonly').show();

    $.getJSON(
        '/status/json/players.json',
        function(data, status, jqXHR) {

            json_data = data;

            class_options = {
                series: {
                    stack: true,
                    lines: {show: false, steps: false },
                    bars: {show: true, barWidth: 0.9, align: 'center',},
                },
                xaxis: {
                    ticks: data.ticks.grad_year
                }
            };

            school_options = {
                series: {
                    stack: true,
                    lines: {show: false, steps: false },
                    bars: {show: true, barWidth: 0.9, align: 'center',},
                },
                xaxis: {
                    ticks: data.ticks.school_id
                }

            };

            dorm_options = {
                series: {
                    stack: true,
                    lines: {show: false, steps: false },
                    bars: {
                        show: true,
                        barWidth: 0.8,
                        align: 'center',
                        horizontal:true
                    },
                },
                yaxis: {
                    ticks: data.ticks.dorm_id
                }
            };
            renderStats();
            window.onresize = function() {
                window.requestAnimationFrame(renderStats);
            };
        });
});
