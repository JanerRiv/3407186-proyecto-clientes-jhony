from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.modelos.clientes import Cliente
from app.modelos.facturas import (
    Factura,
    FacturaCrear,
    FacturaEditar,
    FacturaLeerCompuesta
)
from app.conexion_bd import Sesion_dependencia

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)

# ===================================
# CRUD FACTURAS
# ===================================

# Listar todas las facturas
@router.get("/", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(sesion: Sesion_dependencia):

    lista_facturas = sesion.exec(select(Factura)).all()

    return lista_facturas


# Buscar una factura por ID
@router.get("/{id}", response_model=Factura)
async def listar_factura_id(id: int, sesion: Sesion_dependencia):

    factura_bd = sesion.get(Factura, id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {id} no existe."
        )

    return factura_bd


# Crear una factura
@router.post("/{cliente_id}", response_model=Factura)
async def crear_factura(
    cliente_id: int,
    datos_factura: FacturaCrear,
    sesion: Sesion_dependencia
):

    cliente_bd = sesion.get(Cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con ID {cliente_id} no existe."
        )

    factura_dict = datos_factura.model_dump()

    factura_dict["cliente_id"] = cliente_id

    factura_validada = Factura.model_validate(factura_dict)

    sesion.add(factura_validada)
    sesion.commit()
    sesion.refresh(factura_validada)

    return factura_validada





# Editar una factura
@router.patch("/{id}", response_model=Factura)
async def editar_factura(
    id: int,
    datos_factura: FacturaEditar,
    sesion: Sesion_dependencia
):

    factura_bd = sesion.get(Factura, id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {id} no existe."
        )

    factura_dict = datos_factura.model_dump(exclude_unset=True)

    factura_bd.sqlmodel_update(factura_dict)

    sesion.add(factura_bd)
    sesion.commit()
    sesion.refresh(factura_bd)

    return factura_bd


# Eliminar una factura
@router.delete("/{id}")
async def eliminar_factura(
    id: int,
    sesion: Sesion_dependencia
):

    factura_bd = sesion.get(Factura, id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {id} no existe."
        )

    nombre_cliente = factura_bd.cliente.nombre

    sesion.delete(factura_bd)
    sesion.commit()

    return {
        "mensaje": f"La factura con ID {id} del cliente '{nombre_cliente}' fue eliminada correctamente."
    }