$(document).ready(function() {
    $("#email").blur(function() {
        validateEmail(this.value);
    });
});