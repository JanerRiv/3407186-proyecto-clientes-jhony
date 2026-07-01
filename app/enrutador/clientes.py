from fastapi import APIRouter # APIRouter es una herramienta de FastAPI que permite organizar los endpoints en archivos separados.
from fastapi import HTTPException, FastAPI, status
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.conexion_bd import Sesion_dependencia
from sqlmodel import select

# CONFIGURACIÓN DEL ROUTER


router = APIRouter(       
    prefix="/clientes",  # prefix="/clientes" Agrega automáticamente "/clientes" a todas las rutas
    tags=["Clientes"]    # tags=["Clientes"] permite agrupar los endpoints en la documentaciónSwagger para que aparezcan organizados bajo la categoría "Clientes".
)

# ===================================
# CRUD CLIENTES
# ===================================


@router.get("/", response_model=list[Cliente])
async def listar_cliente(sesion: Sesion_dependencia):
    list_cli = sesion.exec(select(Cliente)).all()
    return list_cli


@router.get("/{id}", response_model=Cliente)
async def listar_cliente_id(id: int, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    return cliente_bd

@router.post("/", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, mi_sesion: Sesion_dependencia):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    mi_sesion.add(cliente_validado)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_validado)
    return cliente_validado


@router.patch("/{id}", response_model=Cliente)
async def editar_cliente(
    id: int,
    datos_cliente: ClienteEditar,
    mi_sesion: Sesion_dependencia
):
    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return cliente_bd

@router.delete("/{id}",  response_model= Cliente)
async def eliminar_cliente(id: int ,mi_sesion: Sesion_dependencia):

    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    return cliente_bd