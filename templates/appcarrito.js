// Creamos nuestra aplicacion.
const miAplicacion = Vue.createApp({
    components: {
        'Añadir': componente1,
        'Lista': componente2,
        'Carrito': componente3,
        'Modificar': componente4,

    },
    data() {
        return {
            Añadir_visible: false,
            Lista_visible: false,
            Carrito_visible: false,
            Modificar_visible: false
        }
    },
    mounted() {
        this.Añadir_visible = true
    },
    methods: {
        show(componente) {
            this.Añadir_visible = false
            this.Lista_visible = false
            this.Carrito_visible = false
            this.Modificar_visible = false
            console.clear()
            console.log(componente)
            if (componente == "Añadir") {
                this.Añadir_visible = true
            } else if (componente == "Lista") {
                this.Lista_visible = true
            } else if (componente == "Carrito") {
                this.Carrito_visible = true
            } else if (componente == "Modificar") {
                this.Modificar_visible = true
            }
        }
    }
}).mount("#app")


const URL = "https://Mariacgznline.pythonanywhere.com/"

const app = Vue.createApp({
    data() {
      return {
        productos: [],
        mostrarCarrito: false,
        carrito: [],
      };
    },
    created() {
      this.obtenerProductos();
    },
    methods: {
      obtenerProductos() {
        fetch(URL + 'productos')
          .then(response => response.json())
          .then(data => {
            this.productos = data;
          })
          .catch(error => {
            console.error(URL + 'productos', error);
            alert('Error al obtener los productos.');
          });
      },
      agregarAlCarrito(producto) {
        fetch(URL + 'carrito', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            codigo: producto.codigo,
            cantidad: 1, // Agregamos una unidad al carrito
          }),
        })
          .then(response => response.json())
          .then(data => {
            alert(data.message);
          })
          .catch(error => {
            console.error('Error al agregar el producto al carrito:', error);
            alert('Error al agregar el producto al carrito.');
          });
      },
      restarDelCarrito(producto) {
        fetch(URL + 'carrito', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            codigo: producto.codigo,
            cantidad: 1, // Restamos una unidad del carrito
          }),
        })
          .then(response => response.json())
          .then(data => {
            alert(data.message);
          })
          .catch(error => {
            console.error('Error al restar el producto del carrito:', error);
            alert('Error al restar el producto del carrito.');
          });
      },
      obtenerCarrito() {
  
        fetch(URL + 'carrito')
          .then(response => response.json())
          .then(data => {
            this.carrito = data;
            this.mostrarCarrito = true;
          })
          .catch(error => {
            console.error('Error al obtener el carrito:', error);
            alert('Error al obtener el carrito.');
          });
      },
    },
  });
  
  app.mount('#appi')