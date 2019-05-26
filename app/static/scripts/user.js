/*
Fetches the number of polls a user has voted in and then
animates the count on their profile page.
*/
$(document).ready(function() {
    fetch(url + "/api/user/" + userID).then(function(response) {
        return(response.json())
    }).then(function(json) {
        voteCounter(json["votes_cast"]);
    })
});

/*
Simple animation function for the vote count on a user's profile page.

Counts upwards from -1 to the number of polls they've voted in with 
a 100ms delay between number changes.
*/
function voteCounter(votes) {
    let current = -1;
    let timer = setInterval(function() {
        current++;
        document.getElementById("vote-counter").textContent = current
        if(current == votes) {
            clearInterval(timer);
        }
    }, 100);
}

