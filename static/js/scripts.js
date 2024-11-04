
const box = document.getElementById("box");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span")
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

menu.addEventListener("click",()=>{
    barraLateral.classList.toggle("max-barra-lateral");
    if(barraLateral.classList.contains("max-barra-lateral")){
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
    }
    else{
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";
    }
    if(window.innerWidth<=320){
        barraLateral.classList.add("mini-barra-lateral");
        main.classList.add("min-main");
        spans.forEach((span)=>{
            span.classList.add("oculto");
        })
    }
});

box.addEventListener('click',()=>{
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach((spans)=>{
        spans.classList.toggle("oculto")
    });
});


// Hora
// Función para actualizar el campo de tipo time basado en el valor de texto
function convertirAHora(horaId, textoId) {
    const textoHora = document.getElementById(textoId).value;
    const inputHora = document.getElementById(horaId);

    // Verificar si el texto tiene el formato correcto (hh:mm)
    const regex = /^([01]?\d|2[0-3]):([0-5]?\d)$/;
    if (regex.test(textoHora)) {
        // Separar horas y minutos y formatear a dos dígitos
        let [horas, minutos] = textoHora.split(':');
        horas = horas.padStart(2, '0');     // Formato 2 dígitos
        minutos = minutos.padStart(2, '0'); // Formato 2 dígitos
        inputHora.value = `${horas}:${minutos}`;
    } else {
        inputHora.value = ''; // Limpiar el campo si el formato es incorrecto
    }
}

// Función para actualizar el campo de texto oculto basado en el valor del campo de tipo time
function convertirHora(horaId, textoId) {
    const inputHora = document.getElementById(horaId).value;
    const horaTexto = document.getElementById(textoId);

    if (inputHora) {
        // Desglosar la hora y los minutos y asignar al campo de texto oculto
        const [horas, minutos] = inputHora.split(':');
        const textoHora = `${horas}:${minutos}`; // Formato "hh:mm"
        horaTexto.value = textoHora;
    }
}




