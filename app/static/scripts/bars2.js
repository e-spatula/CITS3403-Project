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

        return(days, count);
    }).then(function(days, count){
        Object.keys(days).forEach(function(day) {
            // rounds marginal count to nearest multiple of 5.
            let adjustedCount = Math.ceil((days[day] / count /5) * 5);
            $("#bars").append()
        });
    });
});