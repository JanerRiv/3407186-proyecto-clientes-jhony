from pydantic import BaseModel

class ClienteBase(BaseModel):
    #atributos
    nombre : str
    edad: int
    descripcion: str | None

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id : int | None = None