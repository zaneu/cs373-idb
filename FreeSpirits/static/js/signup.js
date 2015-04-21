document.getElementById("btn-login").onclick = function () {
    alert("Login has been clicked");

};

document.getElementById("btn-signup").onclick = function() {
    console.log("In sign up");
    console.log($("#signup-email").val());
    console.log($("#signup-firstname").val() + " " + $("#signup-lastname").val());
    console.log($("#signup-password").val());

    $.post("http://freespirits.me/api/users", {
        email: $("#signup-email").val(),
        firstname: $("#signup-firstname").val() + " " + $("#signup-lastname").text(),
        password: $("#signup-password").val()
    }).done(function (data) {
        alert("User has been successfully created, please login now");
        $('#signupbox').hide();
        $('#loginbox').show();
    }).fail(function (data) {
        alert(data);
    });
};
