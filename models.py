from pydantic import BaseModel

class MyModel(BaseModel):
    name: str
    age: int
    has_pets: bool

