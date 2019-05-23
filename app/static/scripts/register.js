$(document).ready(function() {
    $("#username").blur(function() {
        if(this.value.length == 0) {
            displayText("Username is blank", "error");
        } else {
            fetch(url + "/api/" + this.value).then(function(response) {
                return(response.json());
            }).then(function(json) {
                if(json["response"] === true) {
                    displayText("Username is taken try another one", "error");
                } else {
                    clearText();
                }
            });
        }
    });

    $("#email").blur(function() {
        if(this.value.length === 0) {
            displayText("Email can't be blank", "error");
        } else {
            if(isValidEmail(this.value)) {
                clearText();
            } else {
                displayText("Invalid email address", "error");
            }
        }
    });

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

/* Though it would be possible to use a complex email matching regex pattern, I as the best way to check
if an email is valid is to attempt to send an email to it. This is done on the backend via an email confirmation
link. The check below is more to correct for incompetence than malevolence.
*/
function isValidEmail(email) {
    let re = /.+@.+\..+/g;
    return(re.test(String(email).toLowerCase()));
}

