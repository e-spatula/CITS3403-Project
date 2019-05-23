
$(document).ready(function(){
    $('#menu').load('../pages/nav.html');
});

document.getElementById("menu").onload = function() {loadmenu()}

function loadmenu() {
    document.getElementById("menu").innerHTML = '<object type="text/html" data="../pages/nav.html" ></object>'
}

$("#sidenav").click(function() {
    $(this).style.width = "200px";
});

$("#sidenav").blur(function() {
    document.getElementById("sidenav").style.width = "0";
});
