$(document).ready(function() {
    fetch(url + "/api/user/" + userID).then(function(response) {
        return(response.json())
    }).then(function(json) {
        voteCounter(json["votes_cast"]);
    })
});

function voteCounter(votes) {
    let current = 0;
    let timer = setInterval(function() {
        current++;
        document.getElementById("vote-counter").textContent = current
        if(current == votes) {
            clearInterval(timer);
        }
    }, 100);
}
