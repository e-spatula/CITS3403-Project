/* Simple validation of the PIN.*/
$(document).ready(function() {
    $("#pin").blur(function() {
        validatePin(this.value);
    });
});

