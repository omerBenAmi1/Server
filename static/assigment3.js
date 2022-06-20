
  //write word after word
var i = 0;
var speed = 80;
var txt = "לגלוש, לאכול, להנות !!!";

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("animationP").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}

//nav with active page
const activePge = window.location.href;
const navList = document.querySelectorAll('nav a').forEach(link => {
    if(link.href == activePge){
        console.log(activePge);
        link.classList.add('active');
    }
});

window.onload = typeWriter();


