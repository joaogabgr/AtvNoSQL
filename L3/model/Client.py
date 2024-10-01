from bson import ObjectId
from dataclasses import dataclass, field
from typing import List

@dataclass
class Favorites:
    id_product: ObjectId
    name_product: str
    price_product: float

@dataclass
class Client:
    _id: ObjectId = field(default_factory=ObjectId)
    nameClient: str
    emailClient: str
    passwordClient: str
    ageClient: int
    favorites: List[Favorites] = field(default_factory=list)