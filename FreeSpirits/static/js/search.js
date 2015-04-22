
var host = "http://" + window.location.host;
var search_drinks = true;

$(document).ready(function(){

    //attach a jQuery live event to the button

    $('#searchBtn').on('click', function() {
        if (search_drinks) {
            window.location.href = host + "/search/drinks/" + $('#inputdata').val();
        }
        else {
            window.location.href = host + "/search/ingredients/" + $('#inputdata').val();
        }
    });

    formatText();
    
});

function setToDrinks(value) {
    console.log(value);
    search_drinks = value;
    formatText();
}

function formatText() {
    if (search_drinks) {
        document.getElementById('drinks_text').style.textDecoration = 'underline';
        document.getElementById('drinks_text').style.fontStyle = 'italic';
        document.getElementById('ingredients_text').style.textDecoration = 'none';
        document.getElementById('ingredients_text').style.fontStyle = 'normal';
    }
    else {
        document.getElementById('ingredients_text').style.textDecoration = 'underline';
        document.getElementById('ingredients_text').style.fontStyle = 'italic';
        document.getElementById('drinks_text').style.textDecoration = 'none';
        document.getElementById('drinks_text').style.fontStyle = 'normal';
    }
}
