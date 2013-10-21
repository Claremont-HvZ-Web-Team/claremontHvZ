$(document).ready(function() {
    "use strict";

    var SCHOOL_COLUMN = 1;
    var YEAR_COLUMN = 2;

    function getChosenSchool() {
        return $('#school :selected').val();
    }

    window.filterPlayers = function(players, text, column) {
        var selects = [[SCHOOL_COLUMN, $('#school')], [YEAR_COLUMN, $('#gradyear')]];

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
            var row_data = [];
            for (var j = 0; j < $rows[i].children.length; ++j) {
                row_data.push($rows[i].children[j].textContent);
            }
            data.push(row_data);
        }

        return data;
    }

    function renderTable($table, data) {
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

        var $body = $table.children('tbody');
        $body.children().detach();
        $body.append(html);

        return $table;
    }

    function update(new_human_data, new_zombie_data) {
        renderTable($('#human_list'), new_human_data);
        renderTable($('#zombie_list'), new_zombie_data);

        $('#human_count').text(new_human_data.length);
        $('#zombie_count').text(new_zombie_data.length);
    }

    window.human_data = parseTable($('#human_list'));
    window.zombie_data = parseTable($('#zombie_list'));

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
