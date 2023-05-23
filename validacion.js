const formulario = document.getElementById('formulario');
const nombre = document.getElementById('n');
const apellido = document.getElementById('a');
const telefono = document.getElementById('t');
const email = document.getElementById('m');
const motivo = document.getElementById('mot');
const consulta = document.getElementById('c');

formulario.addEventListener('submit', (e) => {
    e.preventDefault(); //evito que el formulario se envíe antes de validar

    validacion();
    
});


const noValida = (input,mensaje) => {
    const formControl = input.parentElement
    const error = formControl.querySelector('p') //para que el mensaje aparezca en <p></p>
    error.innerText = mensaje //para escribir el mensaje

    formControl.className = 'form-control error' //creo una clase para aplicarle estilos a los bordes del input si no valida
}

const noValidaConsulta = (textarea,mensaje) => {
    const formControl = textarea.parentElement
    const error = formControl.querySelector('p') 
    error.innerText = mensaje 

    formControl.className = 'form-control-consulta error'
}

const siValida = (input,mensaje) => {
    const formControl = input.parentElement

    formControl.className = 'form-control valida' //creo una clase para aplicarle estilos a los bordes del input si valida
}

const siValidaConsulta = (textarea,mensaje) => {
    const formControl = textarea.parentElement

    formControl.className = 'form-control-consulta valida'
}

const validaEMail = (email) => {
    return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
} //uso una expresión regular para validar el mail y el método test  

const validaLetra = (nombre, apellido) => {
    return /^[A-Z]+$/i.test(nombre,apellido);
}

const validaTelefono = (telefono) => {
    return /^[0-9]+$/.test(telefono);
}

const validacion = () =>{
    const nombreValor = nombre.value.trim(); 
    const apellidoValor = apellido.value.trim();
    const telefonoValor = telefono.value.trim(); //.trim elimina los espacios vacíos
    const emailValor = email.value.trim();
    const consultaValor = consulta.value.trim();

//agrego mis condiciones para validar cada uno de los inputs y textarea
    
    if(nombreValor === ''){
        noValida(nombre,'Campo vacío')
    } else if (!validaLetra(nombreValor)) {
        noValida(nombre,'El Nombre no es válido') //valido que el nombre cumpla con la expresión regular (solo letras)
    } else {
        siValida(nombre)
    }

    if(apellidoValor === ''){
        noValida(apellido,'Campo vacío')
    } else if (!validaLetra(apellidoValor)) {
        noValida(apellido,'El Apellido no es válido') //valido que el apellido cumpla con la expresión regular (solo letras)
    }  else{
        siValida(apellido)
    }

    if(telefonoValor === ''){
        noValida(telefono,'Campo vacío')
    } else if (!validaTelefono(telefonoValor)) {
        noValida(telefono,'El Teléfono no es válido') //valido que el teléfono cumpla con la expresión regular (solo números)
    } else if (telefonoValor.length < 10) { //valido que el teléfono tenga como mínimo 10 caracteres 
        noValida(telefono,'Ingrese como mínimo 10 caracteres sin guiones')
    }   else{
        siValida(telefono)
    }

    if(emailValor === ''){
        noValida(email,'Campo vacío') //valido que el mail NO esté vacío 
    } else if (!validaEMail(emailValor)) {
        noValida(email,'El Mail no es válido') //valido que el mail cumpla con la expresión regular 
    } else{
        siValida(email)
    }

    if(consultaValor === ''){
        noValidaConsulta(consulta,'Campo vacío')
    } else{
        siValidaConsulta(consulta)
    }

}



