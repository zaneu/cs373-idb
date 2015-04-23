// Note that the variables starred, item_id, user_id, and star_count
// were defined in a script tag before this executes

var FILLED_STAR = "<span class=\"glyphicon glyphicon-star\" aria-hidden=\"true\"></span>";
var EMPTY_STAR = "<span class=\"glyphicon glyphicon-star-empty\" aria-hidden=\"true\"></span>";

$.support.cors = true;

$(function () {
    function update_counts () {
        $('#unstar-button').html(FILLED_STAR + "Unstar | " + star_count);
        $('#star-button').html(EMPTY_STAR + "Star | " + star_count);
    };

    function update_db () {
        console.log("Inside update db");
        $.post('/api/star/', {
            user_id: user_id,
            item_id: item_id,
            star_count: star_count,
            item_type: item_type
        }).done (function () {
            console.log("Done");
        }).fail (function () {
            console.log("Failed");
        });
    }

    if (starred) {
        $('#unstar-button').show();
        $('#star-button').hide();
    } else {
        $('#star-button').show();
        $('#unstar-button').hide();
    }

    $('#star-button').click(function () {
        star_count += 1;
        update_counts();
        update_db();
        $('#unstar-button').show();
        $('#star-button').hide();
    });

    $("#unstar-button").click(function () {
        star_count -= 1;
        update_counts();
        update_db();
        $('#star-button').show();
        $('#unstar-button').hide();
    });
});
