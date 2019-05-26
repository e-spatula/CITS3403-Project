$(document).ready(function() {
    /*
    Calls validateNewUsername from validate.js
    */
    $("#username").blur(function() {
        validateNewUsername(this.value);
    });
    /*
    Calls validateEmail from validate.js
    */
    $("#email").blur(function() {
        validateEmail(this.value);
    });
      /*
    Validates password.


    Checks if the password is blank and if there is data in the second password field
    checks if the data matches the first field.
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


    Checks if the password is blank and if there is data in the first password field
    checks if the data matches the first field.
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
    /*
    Calls validateImage from validate.js
    */
    $("#display_picture").change(function() {
        validateImage(this.value);
    });
});



