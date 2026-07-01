from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    text: str

class Report(BaseModel):
    title: str
    items: List[Item]
