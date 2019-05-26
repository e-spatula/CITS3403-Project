$(document).ready(function() {
    /*
    Validates password.

    Checks if the password is blank, and if there is data in the second password field 
    checks whether the data matches the current field.
    */
    $("#password").blur(function() {
        let $password2 = $("#password2").val();

        if(this.value.length === 0) {
            displayText("Password can't be blank", "error");
        }
        else if($password2.length > 0 && this.value != $password2) {
            displayText("Passwords must match", "error");
        } else {
            clearText();
        }
    });

    /*
    Validates confirm password.

    Checks if the confirm password is blank, and if there is data in the first password field 
    checks whether the data matches the current field.
    */

    $("#password2").blur(function() {
        let $password = $("#password").val();

        if(this.value.length === 0) {
            displayText("Confirm password can't be blank", "error");
        }
        else if(this.value != $password) {
            displayText("Passwords must match", "error");
        } else {
            clearText();
        }
    });
});
