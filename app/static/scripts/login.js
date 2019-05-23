$(document).ready(function() {
    $("#username").blur(function() {
        validateUsername(this.value);
    });
    $("#password").blur(function() {
        if(this.value.length === 0) {
            displayText("Your password is blank", "error");
        } else {
            clearText();
        }
    });
});