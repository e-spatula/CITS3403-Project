$(document).ready(function(){
    $("#options").children("label").each(function() {
        this.textContent = moment(this.textContent).format("dddd, MMMM Do YYYY, h:mm:ss a");
    });
});