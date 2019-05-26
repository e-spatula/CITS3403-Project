/*
Calls validateEmail from validate.js to validate email.
*/
$(document).ready(function() {
    $("#email").blur(function() {
        validateEmail(this.value);
    });
});
