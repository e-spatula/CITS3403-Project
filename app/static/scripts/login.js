$(document).ready(function() {
    /*
    Calls validateUsername from validate.js
    */
    $("#username").blur(function() {
        validateUsername(this.value);
    });
    /*
    Checks if the password field is blank.
    */
    $("#password").blur(function() {
        if(this.value.length === 0) {
            displayText("Your password is blank", "error");
        } else {
            clearText();
        }
    });
});
