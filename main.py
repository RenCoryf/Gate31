import base64
from dataclasses import dataclass
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing_extensions import Dict
from matcher.app.server import router as match_cloth_router
app = FastAPI()
app.include_router(match_cloth_router)


class Category(Enum):
    UpperClothing = "верхняя одежда"
    Jacket = "жакет"
    Dress = "платье"
    T_shirts = "футболки"
    Hoodies = "худи"
    Bomber = "бомбер"


class Material(Enum):
    Cotton = "хлопок"
    Elastan = "эластан"
    Polyester = "полиэстер"
    Wool = "шерсть"
    Skin = "кожа"


class Style(Enum):
    Casual = "повседрневный"
    Basic = "базовый"
    Evening = "вечерний"
    Office = "офисный"


class Rating(Enum):
    Three = "3"
    Four = "4"
    Five = "5"
    Review = "отзывы"


class Size(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


@dataclass
class MiniCard:
    id: int
    name: str
    price: float
    size: set[Size]
    category: Category
    material: Material
    style: Style
    rating: Rating
    description: str
    color: int
    image: str


class Filters(BaseModel):
    category: Category | None = None
    size: set[Size] | None = None
    color: int | None = None
    material: Material | None = None
    style: Style | None = None
    rating: Rating | None = None
    starting_price: float | None = None
    ending_price: float | None = None


mini_cards: Dict[int, MiniCard] = {}


@app.get("/")
async def root():
    with open("gate31_pics/pic_2.jpg", "rb") as f:
        image_data = f.read()
        image_data = base64.b64encode(image_data).decode("utf-8")
        print(image_data)
        print("HHHHHHHHHHHHHHHHHHH")
    mini_cards[1] = MiniCard(
        id=1,
        category=Category.Hoodies,
        size=set([Size.M, Size.L]),
        color=2,
        material=Material.Cotton,
        style=Style.Casual,
        rating=Rating.Five,
        description="This is a description",
        price=100.0,
        name="Hoodie Red",
        image=image_data,
    )

    mini_cards[2] = MiniCard(
        id=2,
        category=Category.Hoodies,
        size=set([Size.M, Size.L]),
        color=1,
        material=Material.Elastan,
        style=Style.Casual,
        rating=Rating.Four,
        description="This is another description",
        price=150.0,
        name="Hoodie Blue",
        image=image_data,
    )

    print(mini_cards[1])
    print(mini_cards[2])


@app.post("/get_minicards")
async def get_minicards(filters: Filters):
    print(filters.color)
    print("GGGGGGGGGGGGGGGGGGGGGGGG")
    if (
        not filters.category
        and not filters.size
        and not filters.color
        and not filters.material
        and not filters.style
        and not filters.rating
        and not filters.starting_price
        and not filters.ending_price
    ):
        print("GGGGGGGGGGGGGGGGGGGGGGGG")
        print(mini_cards.values())
        return list(mini_cards.values())
    else:
        cards = []
        for card in mini_cards.values():
            if filters.category and card.category != filters.category:
                continue
            if filters.size and card.size != filters.size:
                continue
            if filters.color and card.color != filters.color:
                print(card)
                continue
            if filters.material and card.material != filters.material:
                continue
            if filters.style and card.style != filters.style:
                continue
            if filters.rating and card.rating == filters.rating:
                continue
            if filters.starting_price and card.price < filters.starting_price:
                continue
            if filters.ending_price and card.price > filters.ending_price:
                continue
            cards.append(card)
            return cards
