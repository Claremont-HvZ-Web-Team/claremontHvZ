$(document).ready(function() {
    "use strict";

    var SCHOOL_COLUMN = 1;
    var YEAR_COLUMN = 2;

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
        var html = document.createDocumentFragment();

        for (var i = 0; i < data.length; ++i) {

            var row = document.createElement('tr');

            for (var j = 0; j < data[i].length; ++j) {
                var cell = document.createElement('td');
                cell.textContent = data[i][j];
                row.appendChild(cell);
            }

            html.appendChild(row);
        }

        // If data is empty, instead append the placeholder
        if (data.length === 0) {
            html.appendChild(placeholder);
        }

        var $body = $table.children('tbody');
        $table.fadeOut(function() {
            $body.children().detach();
            $body.append(html);
            $table.fadeIn();
        });

        return $table;
    }

    function update(new_human_data, new_zombie_data) {
        renderTable($('#human_list'), new_human_data, human_placeholder);
        renderTable($('#zombie_list'), new_zombie_data, zombie_placeholder);

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

    var human_cols = human_data[0].length;
    var zombie_cols = zombie_data[0].length;

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
