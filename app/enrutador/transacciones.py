from app.modelos.transacciones import *
from fastapi import APIRouter
from fastapi import HTTPException, FastAPI
from ..listas import Factura
from ..listas import lista_transacciones, lista_facturas,lista_clientes
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select
router = APIRouter(       
    prefix="/transacciones",  
    tags=["Transacciones"]    
)


# ///////////////////////
#CRUD TRANSACCIONES
# ///////////////////////


# ///////////////////////
#VER TRANSACCIONES
# ///////////////////////

@router.get("/transacciones", response_model=list[Transacciones])
def listar_transacciones(sesion: Sesion_dependencia):
    #forma extensa

    #consulta = select(Transacciones)
    #lista_transacciones =sesion.exec(consulta).all()
    #return lista_transacciones

    #forma corta
    return sesion.exec(select(Transacciones)).all()

@router.get("/{id}")
async def obtener_transaccion(id: int):
    pass


# ///////////////////////
#CREAR TRANSACCIONES 
# ///////////////////////

@router.post("/{factura_id}")
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionesCrear, session : Sesion_dependencia):

    
    factura_encontrada = session.get(Factura, factura_id)

    

    if not factura_encontrada:

        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    #Validar datos de la transacción -json y pasamos a dict
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transacciones.model_validate(transaccion_dict)

    #Guardar en BD
    session.add(transaccion_val)
    session.commit()
    session.refresh(transaccion_val)
    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }

  
# Buscamos una transacción específica usando su id.

@router.get("/transacciones/{id}", response_model=Transacciones)
async def obtener_transaccion(id: int):

    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion

    raise HTTPException(
        status_code=404,
        detail="Transacción no encontrada"
    )

# Permite actualizar los datos de una transacción existente.
@router.put("/transacciones/{id}", response_model=Transacciones)
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar
):

    for i, transaccion in enumerate(lista_transacciones):

        if transaccion.id == id:

            transaccion_actualizada = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_actualizada.id = id
            transaccion_actualizada.factura_id = transaccion.factura_id

            lista_transacciones[i] = transaccion_actualizada

            return transaccion_actualizada

    raise HTTPException(
        status_code=404,
        detail="Transacción no encontrada"
    )

# Elimina una transacción de la lista usando su id.
@router.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for transaccion in lista_transacciones:

        if transaccion.id == id:

            lista_transacciones.remove(transaccion)

            return {
                "mensaje": f"Transacción {id} eliminada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Transacción no encontrada"
    )