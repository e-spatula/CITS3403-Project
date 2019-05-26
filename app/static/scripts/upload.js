/* 
Calls validateImage from validate.js
*/
$(document).ready(function() {

    $("#display_picture").change(function() {
        validateImage(this.value);
    });
});
