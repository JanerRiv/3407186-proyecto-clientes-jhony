from app.enrutador.clientes import router as clientes_router
from app.enrutador.facturas import router as facturas_router
from app.enrutador.transacciones import router as transacciones_router
from fastapi import FastAPI
from app.conexion_bd import crear_tablas


app = FastAPI(lifespan= crear_tablas)







app.include_router(clientes_router)
app.include_router(facturas_router)
app.include_router(transacciones_router)


