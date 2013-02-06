(function() {
    "use strict";

    $(function() {
        // Restrict possible dates to the start of the current game and today.
        $("#id_time_0").datepicker({
            minDate: Date.parse($("#game_start")),
            maxDate: new Date(),
        });
    });

})();
