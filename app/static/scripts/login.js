$(document).ready(function() {
    $("#username").blur(function() {
        if(this.value.length === 0) {
            displayText("Your username is blank", "error");
        } else {
            clearText();
        }
    $("#password").blur(function() {
        if(this.value.length === 0) {
            displayText("Your password is blank", "error");
        } else {
            clearText();
        }
    });
    })
});