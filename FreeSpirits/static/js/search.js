
var host = "http://" + window.location.host;

$(document).ready(function(){

    //attach a jQuery live event to the button

    $('#searchBtn').on('click', function() {
            window.location.href = host + "/search/" + $('#inputdata').val();
    });

    formatText();
    
});
