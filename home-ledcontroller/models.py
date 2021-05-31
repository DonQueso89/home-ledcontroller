from pydantic import BaseModel

class Color(BaseModel):
    r: int
    g: int
    b: int
