$(document).ready(function() {
    $("#username").blur(function() {
        validateUsername(this.value);
    });

    $("#pin").blur(function() {
        validatePin(this.value);
    });
});
