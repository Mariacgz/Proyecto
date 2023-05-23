//variables
const boton= document.querySelector('#boton');
const nombre= document.querySelector('#nombre');
const apellido= document.querySelector('#apellido');
const edad= document.querySelector('#edad');
const genero= document.querySelector('#genero');


const generarUusuario = async() => {
    try {
    const url = 'https://randomuser.me/api/?gender=female';
    const respuesta = await fetch(url);
    const {results} =await respuesta.json();
    const datos = results[0];
    console.log(datos);
    foto.src = datos.picture.medium;
    nombre.textContent = datos.name.first;
    apellido.textContent = datos.name.last;
    edad.textContent = datos.dob.age;
    genero.textContent = datos.gender;

    } catch (error) {
        console.log(error)
    }
}

boton.addEventListener('click', generarUusuario);
document.addEventListener('DOMContentLoaded', generarUusuario);