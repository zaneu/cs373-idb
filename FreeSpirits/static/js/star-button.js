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
        $.post('/api/star/', {
            user_id: user_id,
            item_id: item_id,
            star_count: star_count,
            item_type: item_type
        });
    }

    // no current user
    if (user_id < 0) {
        $('button').prop('disabled', true);
    }

    $('#star-button').click(function () {
        star_count += 1;
        update_counts();
        update_db();
        $('#unstar-button').removeClass("hidden");
        $('#star-button').addClass("hidden");
    });

    $("#unstar-button").click(function () {
        star_count -= 1;
        update_counts();
        update_db();
        $('#star-button').removeClass("hidden");
        $('#unstar-button').addClass("hidden");
    });
});
