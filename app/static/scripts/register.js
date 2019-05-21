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

            }
        }
    });
});

function isValidEmail(email) {
    
}

