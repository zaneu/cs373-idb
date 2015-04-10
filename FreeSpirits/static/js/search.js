
var host = "http://" + window.location.host;
var search_drinks = true;

$(document).ready(function(){

    //attach a jQuery live event to the button

    $('#searchBtn').on('click', function() {
            
            if (search_drinks)
                searchDrinks();
            else
                searchIngredients();
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
        //document.getElementById('drinks_text').style.textDecoration = 'underline';
        //document.getElementById('drinks_text').style.fontStyle = 'italic';
        document.getElementById('drinks_text').style.background = '#466279';
        document.getElementById('ingredients_text').style.textDecoration = 'none';
        document.getElementById('ingredients_text').style.fontStyle = 'normal';
        document.getElementById('ingredients_text').style.background = 'none';
        
    }
    else {
        //document.getElementById('ingredients_text').style.textDecoration = 'underline';
        //document.getElementById('ingredients_text').style.fontStyle = 'italic';
        document.getElementById('ingredients_text').style.background = '#466279';
        document.getElementById('drinks_text').style.textDecoration = 'none';
        document.getElementById('drinks_text').style.fontStyle = 'normal';
        document.getElementById('drinks_text').style.background = 'none';
    }
}

function searchDrinks() {
        // alert(host);
        var inputdata = $('#inputdata').val();
        var addr = host + "/drinks/";
        // var count = 0;
        // var list = [];
        // alert(inputdata);
        $.getJSON(host + "/api/drinks", function(data) {
            for(var key in data){
                //console.log(key + "  "+ data[key]);
                if (key.toLowerCase().indexOf(inputdata.toLowerCase()) > -1) {
                    addr = addr + data[key];

                    window.location.href = addr;
                    return;

                }
            }
            window.location.href = host + "/404";
            // alert(data); //uncomment this for debug

        });
}

function searchIngredients() {
        // alert(host);
        var inputdata = $('#inputdata').val();
        var addr = host + "/ingredients/";

        $.getJSON(host + "/api/ingredients", function(data) {
            for(var key in data){
                //console.log(key + "  "+ data[key]);
                if (key.toLowerCase().indexOf(inputdata.toLowerCase()) > -1) {
                    addr = addr + data[key];
                    window.location.href = addr;
                    return;

                }
            }
            window.location.href = host + "/404";
            // alert(addr); //uncomment this for debug

        });
}
