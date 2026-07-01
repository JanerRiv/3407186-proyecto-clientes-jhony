from pydantic import BaseModel
from sqlmodel import SQLModel, Field , Relationship

class TransaccionesBase(SQLModel):
    # atributos
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    descripcion: str | None = Field(default=None)

class TransaccionesCrear(TransaccionesBase):
    pass


class TransaccionesEditar(TransaccionesBase):
    pass


class Transacciones(TransaccionesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion con la tabla factura 
    factura_id: int | None = Field(default=None, foreign_key="factura.id")
    #aqui esta la relacion virtaul con el modelo factura (solo un campo)    
    factura: list["Factura"] = Relationship(back_populates="transacciones")

#crea un modelo para mostrar el usuario o el cliente

class TransaccionLeer(TransaccionesBase):
    id : int
    