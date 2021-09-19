var currSlideIndex = 1;
showSlides(currSlideIndex);

function moveSlides(index) {
    showSlides(currSlideIndex += index);
}

function currentSlide(index) {
    showSlides(currSlideIndex = index);
}
function showText(){
    var x = document.getElementById("myText");
    if(x.innerHTML == ""){
    x.innerHTML = "Your Request has been made! Please wait for assistance.";
    }
}
function showSlides(index) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
   console.log(slides.length)

    if (index > slides.length) {
        currSlideIndex = 1;
    }
    if (index < 1) {
        currSlideIndex = slides.length
    }
    //make all slides invisible
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    //display correct slide
    slides[currSlideIndex - 1].style.display = "block";
}