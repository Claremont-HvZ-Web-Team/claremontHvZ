/**
 * See http://djangosnippets.org/snippets/1053/
 */

jQuery(function($) {
    "use strict";

    var TABLE, POSITION_HEADER, POSITION_INPUT, ROWS;

    TABLE = "#result_list > tbody";
    POSITION_HEADER = "th:contains('Position')";
    POSITION_INPUT = "input[id$=position]"
    ROWS = "#result_list > tbody > tr";

    $(TABLE).sortable({
        update: function() {
            $(this).find("tr").each(function(i) {

                // Switch stripes if the row has changed its parity.
                if (!$(this).hasClass("row" + (i % 2 + 1))) {
                    $(this).toggleClass("row1 row2");
                }

                // Update position of each item
                $(this).find(POSITION_INPUT).val(i+1);
            });

            // Auto-save
            $("input[name=_save]").trigger("click")
        },
    });

    $(ROWS).css('cursor', 'move');
    $(POSITION_HEADER).hide();
    $(POSITION_INPUT).parent().hide();
    $('div.inline-related').find('input[id$=position]').parent('div').hide();
});
