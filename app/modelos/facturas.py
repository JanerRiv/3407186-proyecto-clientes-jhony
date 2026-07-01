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
    #    if not self.transacciones:
        return 0.0

    #    return sum(
    #    t.cantidad * t.vr_unitario
    #    for t in self.transacciones
    #)


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True) :
    
    id: int | None = Field(default=None, primary_key=True)
    #llave foranea en la db
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #creacion de relacion virtual con cliente no en la bd
    cliente : Cliente = Relationship(back_populates="factura")

#crear  modelo para mostrar al usuario o el cliente

class Facturaleer(FacturaBase):
    id: int 
    cliente: ClienteLeer
