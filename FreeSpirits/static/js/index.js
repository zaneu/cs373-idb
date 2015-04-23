$(document).ready(function(){
    var host = "http://" + window.location.host;
    var path = window.location.pathname;

    function redirect_to_index_search () {
        var query = $('#inputdata').val();
        window.location.href = host + "/search/" + query;
    }

    $('#inputdata').keydown (function (event) {
        if (event.keyCode == 13) {
            redirect_to_index_search();
        }
    });

    $('#searchBtn').on('click', function () {
        redirect_to_index_search();
    });
});
