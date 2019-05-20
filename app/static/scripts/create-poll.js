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

function removeDate() {
    let $removedForm = $(".subform").last();
    let removedIndex = parseInt($removedForm.attr("data-index"));

    $removedForm.remove();
    adjustDateIndices(removedIndex);
}

function adjustDateIndices(removedIndex) {
    let $forms = $(".subform");

    $forms.each((function(i) {
        let $form = $(this);
        let index = parseInt($form.data("index"))
        let newIndex = index - 1;
        if(index < removedIndex) {
            return true;
        }
        $form.attr("id", $form.attr("id").replace(index, newIndex));
        $form.data("index", newIndex);
        $form.find("input").each(function(j){
            let $item = $(this);
            $item.attr("id", $item.attr("id").replace(index, newIndex));
            $item.attr("name", $item.attr("name").replace(index, newIndex))
        });
    }));
} 

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

function removeTime() {
    let $parent = $(this).parent();
    let $removedOption = $parent.find("input[type=time]").last();
    
    $removedOption.remove();

}
function formProcessor() {
    $("#errors").empty();
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
    console.log(contents);
    console.log(JSON.stringify(contents));
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

$(document).ready(function() {
    $(".add-date").click(addDate)
    $(".remove-date").click(removeDate);
    $(document).on("click", ".add-time", addTime);
    $(document).on("click", ".remove-time", removeTime);
    $("#submit").click(formProcessor);
});