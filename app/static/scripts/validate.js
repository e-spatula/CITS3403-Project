/*
Validation for new usernames. 

Checks if the username field is blank.


Makes a fetch request to the API to check if a username is already in 
use and displays an error message if it is. 
*/
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
/*
Validation for existing usernames.

Checks if the username field is blank.

Makes a fetch request to the API to check if a username
exists, if not an error is displayed.

*/
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
/*
Validates email addresses.

Checks if an email isn't blank.

Uses a simple regex query to check if the supplied address follows 
the basic format of an email address. e.g. myString@string.com
*/
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

/*
Validates image uploads.

Checks if the extension of a file is supported.
*/
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

/*
Validates admin pins.

Checks if the field isn't empty.

*/
function validatePin(pin) {
    if(pin.length === 0) {
        displayText("PIN is empty", "error");
    } else {
        clearText();
    }
}
