from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field , Relationship
from app.modelos.clientes import Cliente, ClienteLeer
from app.modelos.transacciones import Transacciones
from datetime import datetime

class FacturaBase(SQLModel):
    # atributos
    fecha: str = Field (default= datetime.now()) 
    #cliente: Cliente
    #transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        total_factura = 0.0
        if self.transacciones == None:
            return total_factura
        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad
        return total_factura

class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True) :
    
    id: int | None = Field(default=None, primary_key=True)
    #llave foranea en la db
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #creacion de relacion virtual con cliente, transacciones no en la bd
    cliente : Cliente = Relationship(back_populates="factura")

    transacciones: list[Transacciones] = Relationship(back_populates="factura")
#crear  modelo para mostrar al usuario o el cliente

class Facturaleer(FacturaBase):
    id: int 
    cliente: ClienteLeer
    #se puede agregar a la clase leer pero nop por las buenas practicas

class FacturaLeerCompuesta(Facturaleer):
    transacciones: list[Transacciones] = []
    