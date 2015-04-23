$(document).ready(function(){
    var host = "http://" + window.location.host;
    var path = window.location.pathname;

    function redirect_to_search () {
        var query = $('#nputdata').val();
        window.location.href = host + "/search/" + query;
    }

    $('#inputdata').keydown (function (event) {
        if (event.keyCode == 13) {
            redirect_to_search();
        }
    });

    $('#searchBtn').on('click', function () {
        redirect_to_search();
    });
});
