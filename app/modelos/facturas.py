from pydantic import BaseModel, computed_field

from modelos.clientes import Cliente
from modelos.transacciones import Transacciones


class FacturaBase(BaseModel):
    # atributos
    fecha: str
    cliente: Cliente
    transacciones: list[Transacciones] = []

    @property
    def valor_total(self) -> float:
        if not self.transacciones:
            return 0.0

        return sum(
        t.cantidad * t.vr_unitario
        for t in self.transacciones
    )


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None