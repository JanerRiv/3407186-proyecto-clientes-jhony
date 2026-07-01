from fastapi import APIRouter
from app.modelos.clientes import Cliente 
from app.modelos.facturas import Factura,FacturaCrear,FacturaEditar, Facturaleer, FacturaLeerCompuesta

from datetime import datetime
from fastapi import FastAPI, HTTPException

from ..listas import  lista_facturas
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)

# ///////////////////////
        #CRUD FACTURAS
# ///////////////////////

#///////////////////////
        # ver que faturas se encuentran
# ///////////////////////
@router.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(sesion: Sesion_dependencia ):
    consulta = select(Factura)
    lista_facturas =sesion.exec(consulta).all()
    return lista_facturas

# ///////////////////////
        # CREAR FACTURAS SI EL CLIENTE SE ENCUENTRA
# ///////////////////////


@router.post("/{cliente_id}", response_model=Factura)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    #buscar cliente bd
    cliente_encontrado =  sesion.get(Cliente, cliente_id )
    
    # mensaje si no existe cliente
    
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )

    # validar datos de la factura-json
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)
    
    #guardar en base de datos
    sesion.add(factura_val)
    sesion.commit ()
    sesion.refresh(factura_val)
    return factura_val

# ///////////////////////
#PARA BUSCAR UNA FACTURA POR ID 
# ///////////////////////


@router.get("/{id}", response_model=Factura)
async def obtener_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura

    raise HTTPException(
        status_code=404,
        detail="Factura no encontrada"
    )

# ///////////////////////
#BUSCAR UNA FACTURA DE UN CLIENTE POR SU ID 
# ///////////////////////


@router.get("/clientes/{cliente_id}/facturas")
async def facturas_cliente(cliente_id: int):

    facturas_cliente = [
        f for f in lista_facturas
        if f.cliente.id == cliente_id
    ]

    return facturas_cliente

# ///////////////////////
#EDITAR LA FACTURA 
# ///////////////////////

@router.put("/{id}", response_model=Factura)
async def editar_factura(id: int, datos_factura: FacturaEditar):

    for i, factura in enumerate(lista_facturas):

        if factura.id == id:

            factura_actualizada = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_actualizada.id = id
            factura_actualizada.fecha = factura.fecha
            factura_actualizada.cliente = factura.cliente

            lista_facturas[i] = factura_actualizada

            return factura_actualizada

    raise HTTPException(
        status_code=404,
        detail="Factura no encontrada"
    )

# ///////////////////////
#ELIMINAR LA FACTURA 
# ///////////////////////
@router.delete("/{id}")
async def eliminar_factura(id: int):

    for factura in lista_facturas:

        if factura.id == id:
            lista_facturas.remove(factura)

            return {
                "mensaje": f"Factura {id} eliminada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Factura no encontrada"
    )
