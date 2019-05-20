$(document).ready(function() {
    $("#username").blur(function() {
        if(this.value.length === 0) {
            displayError("Your username is blank");
        } else {
            clearError();
        }
    $("#password").blur(function() {
        if(this.value.length === 0) {
            displayError("Your password is blank");
        } else {
            clearError();
        }
    });
    })
});