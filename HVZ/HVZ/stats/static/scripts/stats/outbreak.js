$(function () {
    "use strict";

    $.getJSON(
        '/status/json/poptimeseries.json',
        function(data, status, jqXHR) {
            console.log("successful stat GET");
            console.log(data);

            var population_holder = "#population_time_series";

            $.plot($(population_holder), data, {});
        }
    );

    $('.noscript').remove();
    $('.scriptonly').show();
});
