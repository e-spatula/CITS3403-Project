window.onload = boxFiller;
function boxFiller() {
    let boxArray  = document.getElementsByClassName("grid-item");
    for(let i = 0; i < boxArray.length; i++) {
        let title = document.createElement("h2");
        let para = document.createElement("p");
        let buttonLink = document.createElement("a");
        let image = document.createElement("img");

        title.className += "grid-title";
        para.className += "grid-text";
        buttonLink.className += "grid-button"
        image.className = "grid-image";

        buttonLink.innerHTML = "Vote";
        buttonLink.href = "https://www.google.com";
        title.innerHTML = "Item " + (i+1);
        para.innerHTML = "Welcome to the " + (i+1)  + " poll";
        image.src = "https://source.unsplash.com/random";
        image.alt = "a random image from unsplash";


        boxArray[i].appendChild(image);
        boxArray[i].appendChild(title);
        boxArray[i].appendChild(para);
        boxArray[i].appendChild(buttonLink);    
    }
    console.log(boxArray[0].innerHTML);
}   