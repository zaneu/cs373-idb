

$(document).ready(function(){
	var host = "http://" + window.location.host;
    //attach a jQuery live event to the button
    $('#searchBtn').on('click', function(){
    	// alert(host);
        var inputdata = $('#inputdata').val();
        var addr = host + "/drinks/";
        // alert(inputdata);
        $.getJSON(host + "/api/drinks", function(data) {
        	for(var key in data){
        		//console.log(key + "  "+ data[key]);
                if (key.toLowerCase().indexOf(inputdata.toLowerCase()) > -1) {
                    addr = addr + data[key];
                    // alert(addr);
                    window.location.replace(addr);
                    return;
                }
        	}

            
            // alert(data); //uncomment this for debug
            //alert (data.item1+" "+data.item2+" "+data.item3); //further debug
            // $('#showdata').html("<p>item1="+data.item1+" item2="+data.item2+" item3="+data.item3+"</p>");
        });
    });
});