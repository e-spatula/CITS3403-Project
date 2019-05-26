/*
Utility function for appending messages to the top of the page. 

Adds an alert banner to the errors div with the category specified.

Takes error, info, success and warning as categories to represent the levels of messaging required
by the application.
*/
function displayText(text, category) {
    $("#errors").empty();
    $("#errors").append("<span class =  'alert-box  banner'> " + text + " </span>");
    $("#errors").children("span").addClass(category);
    document.body.scrollTop = document.documentElement.scrollTop = 0;

}

/*
Clears the error div when messages are no longer needed.
*/
function clearText() {
    $("#errors").empty();
}
