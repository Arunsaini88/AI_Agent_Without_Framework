from pydantic import BaseModel


class ToolAddArgs(BaseModel):
    a: int
    b: int

class ToolMultplyArgs(BaseModel):
    a: int
    b: int