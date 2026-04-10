from pydantic import BaseModel


class ConnectorStatusOut(BaseModel):
    name: str
    mode: str
    status: str
