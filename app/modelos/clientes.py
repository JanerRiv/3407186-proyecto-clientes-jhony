from sqlmodel import SQLModel, Field

class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    edad: int = Field(default=None)
    descripcion: str | None = Field(default=None)

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)