from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.modelos.transacciones import (
    Transacciones,
    TransaccionesCrear,
    TransaccionesEditar
)
from app.modelos.facturas import Factura
from app.conexion_bd import Sesion_dependencia

router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

# ===================================
# CRUD TRANSACCIONES
# ===================================

# Listar todas las transacciones
@router.get("/", response_model=list[Transacciones])
async def listar_transacciones(sesion: Sesion_dependencia):

    lista_transacciones = sesion.exec(select(Transacciones)).all()

    return lista_transacciones


# Buscar una transacción por ID
@router.get("/{id}", response_model=Transacciones)
async def listar_transaccion_id(id: int, sesion: Sesion_dependencia):

    transaccion_bd = sesion.get(Transacciones, id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con ID {id} no existe."
        )

    return transaccion_bd


# Crear una transacción
@router.post("/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionesCrear,
    sesion: Sesion_dependencia
):

    factura_bd = sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {factura_id} no existe."
        )

    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id

    transaccion_validada = Transacciones.model_validate(transaccion_dict)

    sesion.add(transaccion_validada)
    sesion.commit()
    sesion.refresh(transaccion_validada)

    return {
        "mensaje": "Transacción creada correctamente.",
        "transaccion": transaccion_validada
    }


# Editar una transacción
@router.patch("/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar,
    sesion: Sesion_dependencia
):

    transaccion_bd = sesion.get(Transacciones, id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con ID {id} no existe."
        )

    transaccion_dict = datos_transaccion.model_dump(exclude_unset=True)

    transaccion_bd.sqlmodel_update(transaccion_dict)

    sesion.add(transaccion_bd)
    sesion.commit()
    sesion.refresh(transaccion_bd)

    return {
        "mensaje": "Transacción actualizada correctamente.",
        "transaccion": transaccion_bd
    }


# Eliminar una transacción
@router.delete("/{id}")
async def eliminar_transaccion(
    id: int,
    sesion: Sesion_dependencia
):

    transaccion_bd = sesion.get(Transacciones, id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con ID {id} no existe."
        )

    sesion.delete(transaccion_bd)
    sesion.commit()

    return {
        "mensaje": f"La transacción con ID {id} fue eliminada correctamente."
    }