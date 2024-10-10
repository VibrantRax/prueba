
const box = document.getElementById("box");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span")

box.addEventListener('click',()=>{
    barraLateral.classList.toggle("mini-barra-lateral");
    spans.forEach((spans)=>{
        spans.classList.toggle("oculto")
    });
});