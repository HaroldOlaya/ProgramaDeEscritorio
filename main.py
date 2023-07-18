from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db="database/productos.db"

    def __init__(self,root):
        self.ventana=root
        self.ventana.title("App productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/logo.jpg")
        # configurar el frame principal
        frame= LabelFrame(self.ventana,text="Ingresar un nuevo producto")
        frame.grid(row=0,column=0,columnspan=3,pady=20)

        # label nombre
        self.etiqueta_nombre=Label(frame,text="Nombre: ")
        self.etiqueta_nombre.grid(row=1,column=0)

        #entry del nombre
        self.nombre=Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1,column=1)
        
        #label precio
        self.etiqueta_precio=Label(frame,text="Precio: ")
        self.etiqueta_precio.grid(row=2,column=0)

        #entry del precio
        self.precio=Entry(frame)
        self.precio.grid(row=2,column=1)

        #boton de agregar
        self.boton_agregar=ttk.Button(frame,text="AGREGAR",command=self.add_producto)
        self.boton_agregar.grid(row=3,columnspan=2,sticky=W+E)

        self.mensaje=Label(text="",fg="red")
        self.mensaje.grid(row=3,column=0,columnspan=2,sticky=W+E)

        #Tabla productos
        #Estructura de la tabla
        self.tabla=ttk.Treeview(frame,height=20,columns=2)
        self.tabla.grid(row=4,column=0,columnspan=2)
        self.tabla.heading("#0",text="Nombre",anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)

        #botones
        self.boton_eliminar=ttk.Button(text="ELIMINAR",command=self.delProducto)
        self.boton_eliminar.grid(row=5,column=0,sticky=W+E)
        self.boton_editar = ttk.Button(text="EDITAR",command = self.edit_product)
        self.boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()
        
    def dbConsulta(self,consulta,parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor=con.cursor()
            resultado=cursor.execute(consulta, parametros)
            con.commit()
        return resultado
    def get_productos(self):

        registros_tabla=self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query="SELECT * from producto ORDER by nombre desc"
        registros=self.dbConsulta(query)

        for i in registros:
            print(i)
            self.tabla.insert("",0,text=i[1],values=i[2])

    def validacion_nombre(self):
        nombre_introducido=self.nombre.get()
        return len(nombre_introducido)!=0

    def validacion_precio(self):
        precio_introducido = self.precio.get()
        return len(precio_introducido) != 0
    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query="insert into producto values(NULL,?,?)"
            parametros=(self.nombre.get(),self.precio.get())
            self.dbConsulta(query,parametros)
            print("Datos guardados")

            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje["text"]="El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            print("el precio y el nombre son obligatorios")
            self.mensaje["text"] ="el precio y el nombre son obligatorios"

        self.get_productos()

    def delProducto(self):
        print(self.tabla.item(self.tabla.selection()))
        nombre=self.tabla.item(self.tabla.selection())["text"]
        query="delete from producto where nombre=?"
        self.dbConsulta(query,(nombre,))
        self.get_productos()

    def edit_product(self):
        self.mensaje['text']=''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Seleccione un producto'
            return
        nombre=self.tabla.item(self.tabla.selection())['text']
        old_precio=self.tabla.item(self.tabla.selection())['values'][0]#el precio se encuentra dentro de una lista

        self.ventana_editar=Toplevel() #crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)
        # Ventana nueva (editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0, 0)
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri',50, 'bold'))
        titulo.grid(column=0, row=0)
        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto") #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ")#Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)#Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)

        self.input_nombre_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)
        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()#Para que el foco del raton vaya a este Entry al inicio
        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ")#Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0) # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)
        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                     self.input_nombre_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_precio_antiguo.get()))
        self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)

    def actualizar_productos(self,nuevo_nombre,antiguo_nombre,nuevo_precio,antiguo_precio):
        producto_modificado = False
        query = 'UPDATE Producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        if nuevo_nombre != '' and nuevo_precio != '':
            # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
            parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre,antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre,antiguo_precio)
            producto_modificado = True
        if (producto_modificado):
            self.dbConsulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)#mostrar mensaje al usuario



if __name__=="__main__":
    root = Tk() # Instancia de la ventana principal
    app = Producto(root)
    root.mainloop()

