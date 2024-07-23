import json
# Utilizados para instalar el paquete de colorama
import subprocess
import sys

# Creamos la funcion para instalar dependencias 
def install (paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

#Utilizamos un try para ver si el paquete "Colorama" se puede importa, si tira un error, activa la funcion para instalar paquetes "Install"
try:
    import colorama
except ImportError:
    print("Instalando colorama...")
    install("colorama")

# Importa colorama y las funciones que vamos a utilizar de este modulo
from colorama import init, Fore, Back, Style

# Inicializamos colorama
init()

# Colorama sirve para ponerle colores al print en consola, por ejemplo en este trabajo lo utilice para ponerle color rojo a los errores, y color verde a lo agregado.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#


class Productos():
    # Se inicia la clase Producto con lo necesario para conformarla
    def __init__(self, id, nombre, precio, stock):
        # Se asignan los datos propuesto por el usuario
        self.id = id
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = stock
    
    def __str__(self):
        return f"ID: {self.id} - Nombre: {self.nombre} - Precio: ${self.precio:.2f} - Stock: {self.stock}"
    
    def json(self):
        return {
            'id' : self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }

class GestorDeProductos():
    # Se inicia la clase GestorDeProductos con una lista vacia para los productos, un contador en 1 para "ID" de los productos y una funcion que lee el archivo y rellena la lista
    # Si el archivo ya esta creado, lo abre y lee lo que hay dentro para rellenar la lista, si el archivo no esta creado, lo crea vacio.
    def __init__(self):
        self.Lista_productos = []
        self.Cargar_Productos_ARC()
        # Si el archivo ya tiene creado productos, esta funcion lo cuenta y le agrega 1 al valor maximo, sino hay nada cargado el valor es 1
        if self.Lista_productos:
            self.contador = max(producto.id for producto in self.Lista_productos) + 1
        else:
            self.contador = 1
    
    def Agregar_Producto(self, nombre, precio, stock):
        # Utilizamos un try para el manejo de errores, si tiro un error se mostrara en pantalla este y te dira el porque
        try:
            #Hacemos una validacion de los datos, ya que el nombre tiene que ser str, el precio un float, y el stock un entero, ademas de no poder poner numeros negativos.
            precio = float(precio)
            stock = int(stock)
            #Verificamos si "Nombre" es una cadena de texto valida, sino tira un error descriptivo.
            if not isinstance(nombre, str):
                raise ValueError(Fore.RED+"[!] El nombre debe ser una cadena de texto.")
            #Verificamos si "Precio" y "Stock" son numero negativos, sino tira un error descriptivo.
            if precio <= 0 or stock < 0:
                raise ValueError(Fore.RED+"[!] El precio debe ser mayor que cero y el stock debe ser un número entero positivo.")
            
            # Esta condicional, llama a la funcion "Buscar_Producto" para saber si el producto ya esta en la lista, si se encuentra, manda un mensaje por consola de que el producto
            # Ya esta, sino lo agrega, armando el nuevo producto, una vez agregado el producto a la lista, guarda el archivo.
            if not self.Buscar_producto(nombre):
                producto = Productos(self.contador, nombre, precio, stock)
                self.Lista_productos.append(producto)
                self.contador += 1
                self.Guardar_Productos(archivo)
                print(Fore.GREEN+f"[+] Producto '{nombre}' agregado correctamente.")
            #Mensaje de error por si encuentra el producto en la lista.
            else:
                print(Fore.RED+"[!] Este producto ya está en la lista.")
        except ValueError as e:
            print(Fore.RED+f"[!] Error al agregar el producto: {e}") 
            
    def Editar_Producto(self, producto, nombre, precio, stock):
        # Buscamos el producto para saber si existe en la lista o no.
        Producto_OLD = self.Buscar_producto(producto)
        # Si el producto existe entramos a este bloque
        if Producto_OLD:
            # Hacemos un try para verificar si los datos nuevos del producto complen con los requisitos, ("Nombre" = Cadena de texto, "Precio" = Float, "Stock" = Entero)
            try:
                precio = float(precio)
                stock = int(stock)
                if not isinstance(nombre, str):
                    raise ValueError(Fore.RED+"[!] El nombre debe ser una cadena de texto.")
                if precio <= 0 or stock < 0:
                    raise ValueError(Fore.RED+"[!] El precio debe ser mayor que cero y el stock debe ser un número entero positivo.")
                
                # Le asignamos los nuevos valores al producto.
                Producto_OLD.nombre = nombre
                Producto_OLD.precio = precio
                Producto_OLD.stock = stock
                # Se guarda el archivo e imprimi un mensaje de que se edito con exito
                self.Guardar_Productos(archivo)
                print(Fore.GREEN+f"[+] Producto '{producto}' editado correctamente.")
            
            except ValueError as e:
                print(Fore.RED+f"[!] Error al editar el producto: {e}")
        else:
            print(Fore.RED+f"[!] No se encontró ningún producto con '{producto}' para editar.")
        
    def Buscar_producto(self, nombre_o_id):
        # Se define por defecto el "None" en la variable encontrado
        encontrado = None
        
        # verificamos si el dato es un string.
        if isinstance(nombre_o_id, str):
            # iteramos para encontrar el producto dentro de la lista de los productos
            for producto in self.Lista_productos:
                # Convertimos todos los resultados en minisculas para no tener problemas de tipeo
                if producto.nombre.lower() == nombre_o_id.lower():
                    #Si el producto se encuentra cambia el valor de encontrado por el producto.
                    encontrado = producto
                    break
            if encontrado is None:
                return False
        # Lo mismo que arriba, pero con el id, tiene que ser un entero.
        elif isinstance(nombre_o_id, int):
            for producto in self.Lista_productos:
                if producto.id == nombre_o_id:
                    encontrado = producto
                    break
            if encontrado is None:
                return False
        
        return encontrado
    
    def Quitar_Producto(self, id):
        # El argumento esta como "id" pero sirve tanto para el nombre como para el ID
        # Utilizamos la funcion de "Buscar_Producto" para ver si el producto deseado se encuentra en la lista
        producto = self.Buscar_producto(id)
        
        #Si el producto se encuentra, entra al bloque, se elimina de la lista, manda un mensaje por consola de que el producto esta eliminado con exito y guarda el archivo
        if producto:
            self.Lista_productos.remove(producto) 
            print(Fore.RED+f"[-] Producto con ID '{id}' eliminado correctamente.")
            self.Guardar_Productos(archivo)
        # Si el producto no se encuentra en la lista, manda un mensaje por consola diciendo que el producto no se encuentra 
        elif not producto:
            print(Fore.RED+f"[!] No se encontro ningun producto con el ID '{id}' en la lista")            

    
    def mostrar_productos(self):
        # Si la lista esta vacia te imprime el mensaje de que la lista esta vacia
        if not self.Lista_productos:
            print(Fore.RED+"[!] No hay productos para mostrar.")
            return
        # Si tiene productos, se itera por la lista y se imprimen los productos correspondiente
        for producto in self.Lista_productos:
            print(producto)
        
    def Cargar_Productos_ARC(self):
        # Hacemos un try para manejar los posibles errores
        try:
            # Abrimos el archivo en formato de lectura.
            with open(archivo, "r") as f:
                productos_final = json.load(f)
                # Iteramos en el archivo abierto y agregamos todos los productos que esten a la lista en memoria
                for producto in productos_final:
                    producto_obj = Productos(producto['id'], producto['nombre'], producto['precio'], producto['stock'])
                    self.Lista_productos.append(producto_obj)
        except FileNotFoundError:
            print(Fore.BLUE+f"[!+] El archivo '{archivo}' no existe. Se creará uno nuevo.")
        except json.JSONDecodeError as e:
            print(Fore.RED+f"[!] Error al decodificar el archivo JSON: {e}")
        except Exception as e:
            print(Fore.RED+f"[!] Ocurrió un error inesperado al cargar productos: {e}")
    
    def Guardar_Productos(self, archivo):
        # Utilizamos un try para el manejo de posibles errores
        try:
            # Abrimos el archivo en Escritura
            with open(archivo, "w") as f:
                # Transformamos los datos en un objeto iterables, para poder guardarlos en el archivo .json
                productos_final = [producto.json() for producto in self.Lista_productos]
                json.dump(productos_final, f, indent=4)
            print(Fore.GREEN+f"[+] Productos guardados correctamente.")
        except FileNotFoundError:
            print(Fore.RED+f"[!] Error: el archivo '{archivo}' no existe.")
        except json.JSONDecodeError as e:
            print(Fore.RED+f"[!] Error al decodificar el archivo JSON: {e}")
        except Exception as e:
            print(Fore.RED+f"[!] Ocurrió un error inesperado al guardar productos: {e}")
            
    def Opcion_ID_Nombre(self,d):
        # Pasamos lo introducido por el usuario a minisculas para no tener inconsistencias a la hora de comparar.
        if d.lower() == "nombre":
        # Una vez entrado a este bloque, le pide el nombre del producto que desea eliminar al usuario.
            producto = input("¿Como es el nombre del producto que desea editar? -> ")
            return producto
        # Pasamos lo introducido por el usuario a minisculas para no tener inconsistencias a la hora de comparar.
        elif d.lower() == "id":
            # Una vez entrado a este bloque, le pide el ID del producto que desea eliminar al usuario.
            producto = int(input("¿Como es el ID del producto que desea editar? -> "))
            return producto
            
            


            
    def menu(self):
        
        # Bucle while True, es para que el bucle nunca termine hasta que el usuario ponga la opcion 6
        while True:
            
            #Las tres comillas en el print, sirven para poder identar sin problemas, ademas de mostrarlo tal cual esta escrito en el print por consola
            print(Style.RESET_ALL+'''
                ------------- Menu interactivo -------------
                1- Agregar producto
                2- Quitar producto
                3- Editar producto
                4- Buscar producto
                5- Mostrar todos los productos
                6- salir
                ---------------------------------------------''')
            
            # Le pedimos al usuario que ponga la opcion y transformamos el input en entero, ya que a la hora de armar las condiciones, se nos va hacer mas sencillo
            opcion = int(input("¿Que opcion te gustaria elegir? -> "))
            
            # Opcion 1 AGREGAR PRODUCTO
            
            if opcion == 1:
                
                #Aca pedimos los datos necesario para armar un producto, en mi caso serian "Nombre", "Precio", "Stock".
                nombre = input("¿Que nombre le quieres poner al producto? ->")
                precio = input(f"¿Que precio le quieres poner a {nombre}? ->")
                stock = input(f"¿Cuantos {nombre} tienes? -> ")
                # Llamamos la funcion para guardar el producto
                gestor.Agregar_Producto(nombre,precio,stock)
                
            # Opcion 2 QUITAR PRODUCTO
            elif opcion == 2:
                # Esta input sirve para saber si el usuario quiere eliminar el producto por "Nombre" o "ID" esperando que el usuario ponga "Nombre" por si quiere buscar con nombre
                # o "ID" por si quiere buscar por ID
                busqueda = input("¿Como quiere eliminar el producto? [Nombre] o [ID] -> ")
                producto = self.Opcion_ID_Nombre(busqueda)
                # LLama a la funcion "Quitar_Producto" para eliminar el producto seleccionado, se le pasa como argumento lo que el usuario haya elegido el "Nombre" o "ID"
                self.Quitar_Producto(producto)
                
            # Opcion 3 EDITAR PRODUCTO

            elif opcion == 3:
                # Esta input sirve para saber si el usuario quiere eliminar el producto por "Nombre" o "ID" esperando que el usuario ponga "Nombre" por si quiere buscar con nombre
                # o "ID" por si quiere buscar por ID
                busqueda = input("¿Como quiere buscar el producto? [Nombre] o [ID] -> ")
                # Usamos la funcion "Opcion_ID_Nombre" para saber si el usuario quiere buscar el producto por nombre o ID
                producto = self.Opcion_ID_Nombre(busqueda)
                # Le pedimos los datos necesarios para editar el producto
                nombre = input(f"¿Que nombre le quieres poner al producto? ->")
                precio = input(f"¿Que precio le quieres poner a {nombre}? ->")
                stock = input(f"¿Cuantos {nombre} tienes? -> ")
                #Utilizamos la funcion "Editar_Producto" para editar y guardar el producto.
                self.Editar_Producto(producto,nombre,precio,stock )
                
            # Opcion 4 BUSCAR PRODUCTO POR NOMBRE O ID Y MOSTRARLO EN CONSOLA
            elif opcion == 4:   
                # Esta input sirve para saber si el usuario quiere eliminar el producto por "Nombre" o "ID" esperando que el usuario ponga "Nombre" por si quiere buscar con nombre
                # o "ID" por si quiere buscar por ID
                busqueda = input("¿Como quiere buscar el producto? [Nombre] o [ID] -> ")
                # Usamos la funcion "Opcion_ID_Nombre" para saber si el usuario quiere buscar el producto por nombre o ID
                producto = self.Opcion_ID_Nombre(busqueda)
                # Usamos la fucion "Buscar_Producto" para encontrar el producto indicado             
                resultado = self.Buscar_producto(producto)
                # Si el producto es encontrado, te lo muestra por consola.
                if resultado:
                    print(resultado)
                # Si el producto no es encontrado, se muestra por consola un mensaje de que el producto no esta en la lista.
                elif resultado == False:
                    print(Fore.RED+"[!]Este producto no se encuentra en la lista")
                    
            # Opcion 5 MOSTRAR TODOS LOS PRODUCTOS POR CONSOLA
            elif opcion == 5:
                self.mostrar_productos()
                
            # Opcion 6 SALIR DEL PROGRAMA
            elif opcion == 6:
                print(Fore.RED+"[!] Saliendo del programa...")
                break
        
        

if __name__ == "__main__":
    # Se le pide el nombre del archivo al usuario
    archivo = input("¿Que nombre te gustaria ponerle al archivo? -> ")
    # Se le agrega la extension .json
    archivo = (f"{archivo}.json")
    # Se crea Gestor De Productos
    gestor = GestorDeProductos()
    # Llama a la funcion Guardar_Productos para que el archivo se cree (Vacio)
    gestor.Guardar_Productos(archivo)
    # Se llama la funcion "Menu" para que se muestre el menu en consola
    gestor.menu()
    