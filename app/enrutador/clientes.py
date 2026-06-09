from fastapi import APIRouter # APIRouter es una herramienta de FastAPI que permite organizar los endpoints en archivos separados.

from modelos.clientes import Cliente,ClienteCrear,ClienteEditar

from conexion_bd import lista_clientes


# CONFIGURACIÓN DEL ROUTER


router = APIRouter(       
    prefix="/clientes",  # prefix="/clientes" Agrega automáticamente "/clientes" a todas las rutas
    tags=["Clientes"]    # tags=["Clientes"] permite agrupar los endpoints en la documentaciónSwagger para que aparezcan organizados bajo la categoría "Clientes".
)

#CRUD CLIENTES

@router.get("/")
def listar_clientes():

    if len(lista_clientes) == 0:
        return {"mensaje": "No hay clientes registrados"}

    else:
        return {"clientes": lista_clientes}
    
@router.get("/{id}")
async def listar_cliente(id: int):
    # retornar mensajes claros al usuario, si no existe el cliente
    # return [d for d in lista_clientes if d.id ==id]
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente


@router.post("/", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes) + 1  # id incremento
    lista_clientes.append(cliente_val)
    return cliente_val
    # return {"Cliente": cliente_val}

@router.put("/{id}")
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


@router.delete("/")
def eliminar_clientes (id:int):
    for cliente  in lista_clientes:
        if cliente.id ==  id:
            lista_clientes.remove(cliente)
            return {"mensaje": f"cliente {cliente.nombre, cliente.descripcion} eliminado"}
        
    return ("mensaje:cliente no encontrado")
