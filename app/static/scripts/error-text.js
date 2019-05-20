function displayError(errorText) {
    $("#errors").empty();
    $("#errors").append("<span class =  'alert-box error banner'> " + errorText + " </span>");
    document.body.scrollTop = document.documentElement.scrollTop = 0;

}

function clearError() {
    $("#errors").empty();
}