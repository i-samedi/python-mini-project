from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('Libreta de Clientes')

conn = sqlite3.connect('crm.db')
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        empresa TEXT NOT NULL
        );
          """)

def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))
        
def insertar(cliente):
    c.execute("""INSERT INTO cliente (nombre, telefono, empresa) VALUES (?, ?, ?)""", 
              (cliente['nombre'], cliente['telefono'], cliente['empresa']))
    conn.commit()
    render_clientes()
    
def nuevo_clientes():
    def guardar():
        if not nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        if not telefono.get():
            messagebox.showerror('Error', 'El telefono es obligatorio')
            return
        if not empresa.get():
            messagebox.showerror('Error', 'La empresa es obligatoria')
            return
        cliente = {
            'nombre' : nombre.get(),
            'telefono' : telefono.get(),
            'empresa' : empresa.get()
        }
        insertar(cliente)
        top.destroy()
    
    top = Toplevel()
    top.title('Nuevo Cliente')
    
    lnombre = Label(top, text = 'Nombre')
    nombre = Entry(top, width=40)
    lnombre.grid(column=0, row=0)
    nombre.grid(column=1, row=0)
    
    ltelefono = Label(top, text = 'Telefono')
    telefono = Entry(top, width=40)
    ltelefono.grid(column=0, row=1)
    telefono.grid(column=1, row=1)   
    
    lempresa = Label(top, text = 'Empresa')
    empresa = Entry(top, width=40)
    lempresa.grid(column=0, row=2)
    empresa.grid(column=1, row=2)
    
    guardar = Button(top, text='Guardar', command=guardar)
    guardar.grid(column=1, row=3)
    top.mainloop()
    
def eliminar_clientes():
    selections = tree.selection()
    if not selections:
        messagebox.showerror('Error', 'Selecciona al menos un cliente')
        return
    
    for selection in selections:
        c.execute("DELETE FROM cliente WHERE id=?", (selection,))
    conn.commit()
    render_clientes()
        
btn = Button(root, text='Nuevo Cliente', command=lambda: nuevo_clientes())
btn.grid(column=0, row=0)
btn = Button(root, text='Eliminar Cliente', command=lambda: eliminar_clientes())
btn.grid(column=1, row=0)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Telefono', 'Empresa')
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text = 'Nombre')
tree.heading('Telefono', text = 'Telefono')
tree.heading('Empresa', text = 'Empresa')
tree.grid(column=0, row=1, columnspan=2)

root.mainloop()