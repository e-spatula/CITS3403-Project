
$(document).ready(function(){
    $('#menu').load('../pages/nav.html');
});

document.getElementById("menu").onload = function() {loadmenu()}

function loadmenu() {
    document.getElementById("menu").innerHTML = '<object type="text/html" data="../pages/nav.html" ></object>'
}
