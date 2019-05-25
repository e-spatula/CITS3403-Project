$(document).ready(function() {
    $("#pin").blur(function() {
        validatePin(this.value);
    });
});
