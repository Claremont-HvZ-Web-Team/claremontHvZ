$(document).ready(function() {
    "use strict";

    var SCHOOL_COLUMN = 1;
    var YEAR_COLUMN = 2;

    var HUMAN_COLS = 4;
    var ZOMBIE_COLS = 5;

    function filterPlayers(players, text, column) {
        var selects = [
            [SCHOOL_COLUMN, $('#school')],
            [YEAR_COLUMN, $('#gradyear')],
        ];

        for (var i = 0; i < selects.length; ++i) {
            var column = selects[i][0];
            var text = selects[i][1].val();

            if (!text) {
                continue;
            }

            players = players.filter(function(player) {
                return player[column] === text;
            });
        }

        return players;
    }

    function parseTable($table) {
        var $rows = $table.children('tbody').children('tr');

        var data = [];
        for (var i = 0; i < $rows.length; ++i) {

            // Don't include the "no humans/zombies!" placeholder
            if ($rows[i].classList.contains("placeholder")) {
                continue;
            }

            var row_data = [];
            for (var j = 0; j < $rows[i].children.length; ++j) {
                row_data.push($rows[i].children[j].textContent);
            }
            data.push(row_data);
        }

        return data;
    }

    function renderTable($table, data, placeholder) {
        // If data is empty, append the placeholder
        if (data.length === 0) {
            $table.children('tbody').append(placeholder);
        } else {
            $table.children('tbody').children('tr.placeholder').detach();
        }

        var $rows = $table.children('tbody').children('tr');

        // This assumes the data is in the same order as the HTML rows.
        var i = 0;
        $rows.each(function() {
            if ($(this).hasClass('placeholder')) {
                return;
            }

            if (i < data.length && this.children[0].textContent === data[i][0]) {
                $(this).removeClass('hidden');
                $(this).addClass('visible');

                if (i % 2 === 0) {
                    $(this).addClass('even');
                    $(this).removeClass('odd');
                } else {
                    $(this).removeClass('even');
                    $(this).addClass('odd');
                }

                ++i;
            } else {
                $(this).addClass('hidden');
                $(this).removeClass('visible');
            }
        });

        return $table;
    }

    function update(new_human_data, new_zombie_data) {
        $('#human_list').fadeOut(function() {
            renderTable($(this), new_human_data, human_placeholder);
            $(this).fadeIn();
        });

        $('#zombie_list').fadeOut(function() {
            renderTable($(this), new_zombie_data, zombie_placeholder);
            $(this).fadeIn();
        });

        $('#human_count').fadeOut(function() {
            $(this).text(new_human_data.length);
            $(this).fadeIn();
        });
        $('#zombie_count').fadeOut(function() {
            $(this).text(new_zombie_data.length);
            $(this).fadeIn();
        });
    }

    var human_data = parseTable($('#human_list'));
    var zombie_data = parseTable($('#zombie_list'));

    // Magic values to handle the empty case
    var human_cols = human_data.length > 0 ? human_data[0].length : HUMAN_COLS;
    var zombie_cols = zombie_data.length > 0 ? zombie_data[0].length : ZOMBIE_COLS;

    var placeholders = [
        [human_cols, "There aren't any humans!"],
        [zombie_cols, "There aren't any zombies!"],
    ].map(function(pair) {
        var placeholder = document.createElement('tr');
        placeholder.classList.add('placeholder');

        var td = document.createElement('td');
        td.setAttribute('colspan', pair[0]);
        td.textContent = pair[1];
        placeholder.appendChild(td);
        return placeholder;
    });

    var human_placeholder = placeholders[0];
    var zombie_placeholder = placeholders[1];

    $('#school').change(function(event) {
        var new_human_data = filterPlayers(human_data);
        var new_zombie_data = filterPlayers(zombie_data);
        update(new_human_data, new_zombie_data);
    });

    $('#gradyear').change(function(event) {
        var new_human_data = filterPlayers(human_data);
        var new_zombie_data = filterPlayers(zombie_data);
        update(new_human_data, new_zombie_data);
    });

	$('.noscript').remove();
});
