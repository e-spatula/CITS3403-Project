function validateNewUsername(username) {

    if(username.length == 0) {
        displayText("Username is blank", "error");
    } else {
        fetch(url + "/api/" + username).then(function(response) {
            return(response.json());
        }).then(function(json) {
            if(json["response"] === true) {
                displayText("Username is taken try another one", "error");
            } else {
                clearText();
            }
        });
    }
}

function validateUsername(username) {
    if(username.length == 0) {
        displayText("Username is blank", "error");
    } else {
        fetch(url + "/api/" + username).then(function(response) {
            return(response.json());
        }).then(function(json) {
            if(json["response"] === false) {
                displayText("Username doesn't exist", "error");
            } else {
                clearText();
            }
        });
    }
}
function validateEmail(email) {
    if(email.length === 0) {
        displayText("Email can't be blank", "error");
    } else {
        if(isValidEmail(email)) {
            clearText();
        } else {
            displayText("Invalid email address", "error");
        }
    }
}

function validateImage(image) {
    let extension = image.split(".").pop();
        if(!allowed_files.includes(extension)) {
            displayText("Unsupported file type", "error");
        } else {
            clearText();
        }
}

/* Though it would be possible to use a complex email matching regex pattern, I as the best way to check
if an email is valid is to attempt to send an email to it. This is done on the backend via an email confirmation
link. The check below is more to correct for incompetence than malevolence.
*/
function isValidEmail(email) {
    let re = /.+@.+\..+/g;
    return(re.test(String(email).toLowerCase()));
}

function validatePin(pin) {
    if(pin.length === 0) {
        displayText("PIN is empty", "error");
    } else {
        clearText();
    }
}