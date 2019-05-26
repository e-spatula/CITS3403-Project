$(document).ready(function(){
    /*
    Reformats the dates on the poll page from ugly python date stamps to
    nice dates using moment.js.
    */
    $("#options").children("label").each(function() {
        this.textContent = moment(this.textContent).format("dddd, MMMM Do YYYY, h:mm:ss a");
    });
});
