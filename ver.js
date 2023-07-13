const url = 'https://geny.pythonanywhere.com/productos';
const data = {
codigo: 4,
descripcion: 'Producto 4',
cantidad: 20,
precio: 49.99
};
fetch(url, {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify(data)
})
.then(response => {
if (response.ok) {
console.log('Producto agregado correctamente');
} else {
console.log('Error al agregar el producto');
}
})
.catch(error => {
console.error('Error de conexión:', error);
});