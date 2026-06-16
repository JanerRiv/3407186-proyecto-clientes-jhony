
from enrutador.clientes import router as clientes_router
from enrutador.facturas import router as facturas_router
from enrutador.transacciones import router as transacciones_router
from fastapi import FastAPI


app = FastAPI()







app.include_router(clientes_router)
app.include_router(facturas_router)
app.include_router(transacciones_router)


