$(document).ready(function() {

    $("#display_picture").change(function() {
        let extension = this.value.split(".").pop();
        if(!allowed_files.includes(extension)) {
            displayText("Unsupported file type", "error");
        } else {
            clearText();
        }
    });
});