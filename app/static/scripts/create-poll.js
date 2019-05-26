/*
Function for adding a date.

Clones a hidden template at the bottom of the page and appends it to the subform container. 
Checks to see if more than 5 dates have been adeed and maintains consistent indices for the dates.


*/
function addDate() {
    let $templateForm = $("#options-_");
    if(!$templateForm) {
        console.log("No template found");
    }
    let newIndex = 0;
    let $lastForm = $(".subform").last();
    let $newForm  = $templateForm.clone();
    if($lastForm.length > 0) {
        newIndex = parseInt($lastForm.data("index")) + 1;
    }
    if(newIndex > 4) {
        displayText("Can't add more than 5 dates", "error");
        return false;
    }
    $newForm.attr("id", $newForm.attr("id").replace("_", newIndex));
    $newForm.attr("data-index", newIndex);

    $newForm.find("input").each(function(idx) {
        let $item = $(this);
        $item.attr("id", $item.attr("id").replace("_", newIndex));
        $item.attr("name", $item.attr=("name").replace("_", newIndex));
    });
    $newForm.append("<input id='options-" + newIndex +"-times-0-time' required type='time' value='' data-index = '0'>");
    $newForm.append("<br>");
    $("#subform-container").append($newForm);
    
    $newForm.addClass("subform");
    $newForm.removeClass("is-hidden");
}

/*
Removes a date.

Selects the last instance of the subform class and removes it. 
*/
function removeDate() {
    let $removedForm = $(".subform").last();
    let removedIndex = parseInt($removedForm.attr("data-index"));

    $removedForm.remove();
}


/*
Adds a time to date.

Clones the previous sibling of its parent element to add a time element. 
If there is no previous sibling a new time element is constructed.

Checks if more than 5 times have been added to a date and displays an error message
if the user attempts to add more than 5 times to the same date.
*/
function addTime() {
    let $currentForm = $(this).parent();
    let parentID = $currentForm.attr("data-index");
    let newID = 0;
    let $previousSibling = $currentForm.find("input[type=time]").last();
    // If there is no previous sibling construct a new time element 
    if($previousSibling.length == 0) {
        $currentForm.append("<input id='options-" + parentID + "-times-0-time' required type='time' value='' data-index = '0'>");
        return true;
    }
    let previousID = parseInt($previousSibling.attr("data-index"));
    newID = previousID + 1;

    if(newID > 4)  {
        displayText("Can't add more than 5 times to a date", "error");
        return false;
    }
    let $newElement =  $previousSibling.clone();
    $newElement.attr("id", $newElement.attr("id").replace("times-" + previousID, "times-" + newID))
    $newElement.attr("data-index", newID);
    $currentForm.append($newElement);
    $currentForm.append("<br>");
    
}

/*
Removes a time

Finds the last child of the parent that is a time input and removes it.
*/
function removeTime() {
    let $parent = $(this).parent();
    let $removedOption = $parent.find("input[type=time]").last();
    
    $removedOption.remove();

}
/*
Validates the form, packages it up into JSON and posts it to the backend.

Checks if the form doesn't have a title or if the description is more than 240 characters.

Checks if the expiry date is not set or is set in the past.

Checks that all the dates and times submitted are valid.

Breaks down the dates and times into their individual components and reconstructs them
as datetime stamps for passing to the backend. 

Checks if at least one option has been created. 


*/
function formProcessor() {
    contents = {};
    let title = $("#title").val();
    if(!title) {
        displayText("Your poll doesn't have a title", "error");
        return false;
    }
    let description = $("#description").val();
    if(description.length > 240) {
        displayText("Can't have a description longer than 240 characters", "error");
        return false;
    }
    let expiry_date = $("#expiry_date").val();
    expiry_date = new Date(expiry_date.replace(/-/g, "/")).getTime();
    let today = new Date()

    // check if there is no date or that it is before today

    if(!expiry_date || expiry_date < today) {
        displayText("Expiry date blank or set in the past", "error");
        return false;
    }
    let options_limit = $("#options_limit option:selected").val();
    contents["options_limit"] = options_limit;
    contents["title"] = title;
    contents["description"] = description;
    contents["expiry_date"] = expiry_date;

    // create empty array to contain options
    let options = [];
    // iterate through the subforms
    $("#subform-container").find("div").each(function(i) {
        let date = $(this).find("input[type=date]").first().val();
        // change date format for easier comparison with JS Date
        date = date.replace(/-/g, "/");
        if(!date || new Date(date) < new Date()) {
            displayText("Can't have blank dates or set options in the past, have a look at date " + (i + 1), "error");
            return false;
        }
        // Decompose date features into individual components
        splitDate = date.split("/");
        splitDate.forEach(function(item) {
            if(item.charAt(0) === "0") {
                item = item.slice(0, item.length);
            }
            item = parseInt(item);
        });
        let year = splitDate[0];
        let month = splitDate[1];
        let day = splitDate[2];
        // fix for the fact that JS decides to index months from 0
        month--;
        // loop through time elements of each date
        $(this).find("input[type=time]").each(function(j) {
            let time = $(this).val();
            if(!time) {
                displayText("You can't leave blank times, have a look at date " + (i  + 1 )+ " time " + (j + 1), "error");
                return false;
            }
            // decompose time into hours and minutes and strip leading zeros
            let splitTime = time.split(":");
            splitTime.forEach(function(item) {

                if(item.charAt(0) === "0") {
                    item = item.slice(0, item.length);
                }
                item = parseInt(item);
            })
            let hour =  splitTime[0];
            let minute = splitTime[1];
            let dateTime = new Date(year, month, day, hour, minute).getTime();
            options.push(dateTime);
        })
    });
    if(options.length == 0) {
        displayText("You haven't added any options", "error");
        return false;
    }
    contents["options"] = options;
    let headers = {
        "Content-Type" : "application/json"
    }
    let url = window.location.href;

    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(contents)
    }).then(function(response) {
        return(response.json());
    }).then(function(json) {
        let pollUrl = json["url"];
        // checking to see if the URL to the poll is false, meaning that there was an error on the backend.
        if(pollUrl) {
            url = url.substring(0, url.lastIndexOf("/") + 1);
            url = url + pollUrl;
            window.location.replace(url);
        } else {
            displayText("Please enable your Javascript for form validation", "error");
        }
        
        
    });

}

/*
Adds all the necessary event listeners 
*/
$(document).ready(function() {
    $(".add-date").click(addDate)
    $(".remove-date").click(removeDate);
    $(document).on("click", ".add-time", addTime);
    $(document).on("click", ".remove-time", removeTime);
    $("#submit").click(formProcessor);
});
