function displayText(text, category) {
    $("#errors").empty();
    // $("#errors").append($("span").addClass("alert-box banner" + category).text(text));
    $("#errors").append("<span class =  'alert-box  banner'> " + text + " </span>");
    $("#errors").children("span").addClass(category);
    document.body.scrollTop = document.documentElement.scrollTop = 0;

}

function clearText() {
    $("#errors").empty();
}