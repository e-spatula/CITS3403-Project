        fetch(url + "/api/" + this.value).then(function(response) {
            return(response.json());
        }).then(function(json) {
            if(json["response"] === true) {
                displayText("Username is taken try another one", "error");
            }
        });