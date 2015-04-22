// Note that the variables starred, drink_id, user_id, and star_count
// were defined in a script tag before this executes

var FILLED_STAR = "<span class=\"glyphicon glyphicon-star\" aria-hidden=\"true\"></span>";
var EMPTY_STAR = "<span class=\"glyphicon glyphicon-star-empty\" aria-hidden=\"true\"></span>";

$(function () {
    function update_counts () {
        $('#unstar-button').html(FILLED_STAR + "Unstar | " + star_count);
        $('#star-button').html(EMPTY_STAR + "Star | " + star_count);
    };

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
        $('#unstar-button').show();
        $('#star-button').hide();
    });

    $("#unstar-button").click(function () {
        star_count -= 1;
        update_counts();
        $('#star-button').show();
        $('#unstar-button').hide();
    });
});
