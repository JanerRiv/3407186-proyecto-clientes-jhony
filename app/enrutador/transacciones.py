from app.modelos.transacciones import *
from fastapi import APIRouter
from fastapi import HTTPException, FastAPI
from ..listas import lista_transacciones, lista_facturas,lista_clientes

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

@router.get("/TRANSACCIONES")
def listar_TRANSACCIONES():

    if len(lista_transacciones) == 0:
        return {"mensaje": "No hay transacciones"}

    else:
        return {"transacciones": lista_transacciones}

# ///////////////////////
#CREAR TRANSACCIONES 
# ///////////////////////

@router.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int
):

    # Buscamos el cliente para confirmar que está registrado antes de crear la transacción.
    cliente_encontrado = None

    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # Si el cliente no existe, mostramos un mensaje indicando que primero debe registrarse.
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )

    # Buscamos si ya existe una factura con el id recibido.
    factura_encontrada = None

    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break

    # Si encontramos la factura continuamos con el proceso.
    if factura_encontrada:

        # Verificamos que la factura realmente pertenezca al cliente indicado.
        if factura_encontrada.cliente.id == cliente_id:

            # Validamos los datos recibidos y creamos la nueva transacción.
            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            # Asignamos un id consecutivo a la transacción.
            transaccion_val.id = len(lista_transacciones) + 1

            # Relacionamos la transacción con la factura correspondiente.
            transaccion_val.factura_id = factura_id

            # Guardamos la transacción en la lista general.
            lista_transacciones.append(transaccion_val)

            # También agregamos la transacción dentro de la factura encontrada.
            factura_encontrada.transacciones.append(transaccion_val)

            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada

            return {
                "mensaje": mensaje,
                "factura": factura_final
            }

        # Si la factura existe pero pertenece a otro cliente, informamos la situación.
        else:

            mensaje = (
                f"Se encontro la factura de id: {factura_id}, "
                f"pero es de otro cliente id: {cliente_id}"
            )

            factura_final = factura_encontrada

            return {
                "mensaje": mensaje,
                "factura encontrada": factura_final
            }

    '''# Si no existe la factura, creamos una nueva junto con la transacción.
    else:

        # Validamos los datos de la transacción.
        transaccion_val = Transacciones.model_validate(
            datos_transaccion.model_dump()
        )

        # Generamos el id de la transacción.
        transaccion_val.id = len(lista_transacciones) + 1

        # Relacionamos la transacción con la nueva factura que se va a crear.
        transaccion_val.factura_id = len(lista_facturas) + 1

        # Creamos la factura con el cliente, la fecha actual y la transacción registrada.
        factura = FacturaCrear(
            cliente=cliente_encontrado,
            fecha=str(datetime.now()),
            transacciones=[transaccion_val],
        )

        # Convertimos los datos al modelo Factura.
        factura_val = Factura.model_validate(factura.model_dump())

        # Asignamos un id a la nueva factura.
        factura_val.id = len(lista_facturas) + 1

        # Guardamos la factura en la lista de facturas.
        lista_facturas.append(factura_val)

        # Guardamos también la transacción en la lista general.
        lista_transacciones.append(transaccion_val)

        return {
            "mensaje": f"Factura no existe con el id: {factura_id}, pero se creo la nueva factura",
            "facturas": transaccion_val,
        }'''
    
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