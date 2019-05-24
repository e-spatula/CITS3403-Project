$(document).ready(function() {
    fetch(url + "/api/poll/" + String(poll_id)).then(function(response) {
        return(response.json());
    }).then(function(json) {
        let count = json["votes_count"];
        let options = json["options"];
        let days = {};
        Object.keys(options).forEach(function(day) {
            formattedDay = moment(day).format("MMM Do YYYY");
            if(formattedDay in Object.keys(days)) {
                days[formattedDay] += parseInt(options[day])
            } else {
                days[formattedDay] = parseInt(options[day]);  
            }
        });

        Object.keys(days).forEach(function(day) {
            let adjustedCount = (days[day] / count);
            adjustedCount = adjustedCount * 100;
            let barDiv = document.createElement("div");
            let labelSpan = document.createElement("span");

            labelSpan.className += "graphColumnLabel";
            labelSpan.innerHTML = day;

            barDiv.className += "graphBar ";
            barDiv.className += "h" + adjustedCount;
            
            document.getElementById("labels").appendChild(labelSpan)
            document.getElementById("bars").appendChild(barDiv);
            console.log(adjustedCount);
        });
    });
});