from datetime import datetime

from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import FacturaBase,FacturaCrear,FacturaEditar,Factura
from modelos.transacciones import Transacciones,TransaccionesBase,TransaccionesCrear,TransaccionesEditar
app = FastAPI()

# lista de clientes en BD
lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones]

#CRUD CLIENTES

@app.get("/clientes")
def listar_clientes():

    if len(lista_clientes) == 0:
        return {"mensaje": "No hay clientes registrados"}

    else:
        return {"clientes": lista_clientes}


@app.get("/clientes/{id}")
async def listar_cliente(id: int):
    # retornar mensajes claros al usuario, si no existe el cliente
    # return [d for d in lista_clientes if d.id ==id]
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente


@app.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes) + 1  # id incremento
    lista_clientes.append(cliente_val)
    return cliente_val
    # return {"Cliente": cliente_val}


@app.put("/clientes/{id}")
def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val

    return {
        "mensaje": "Se actualizo el cliente satisfactoriamente.",
        "Cliente": cliente_val,
    }


@app.delete("/clientes")
def eliminar_clientes (id:int):
    for cliente  in lista_clientes:
        if cliente.id ==  id:
            lista_clientes.remove(cliente)
            return {"mensaje": f"cliente {cliente.nombre, cliente.descripcion} eliminado"}
        
    return ("mensaje:cliente no encontrado")

# ///////////////////////
        #CRUD FACTURAS
# ///////////////////////


@app.get("/facturas")
async def listar_facturas():
    if len(lista_facturas) == 0:
            return {"mensaje": "No hay facturas registradas"}

    else:
        return lista_facturas
    

@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    # cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # si no existe cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )

    # crear la factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val