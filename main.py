import base64
import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing_extensions import Dict

from matcher.app.server import router as match_cloth_router
from pic_giver import get_picture

app = FastAPI()
app.include_router(match_cloth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    category: set[Category] | None = None
    size: set[Size] | None = None
    color: set[int] | None = None
    material: set[Material] | None = None
    style: set[Style] | None = None
    rating: set[Rating] | None = None
    starting_price: float | None = None
    ending_price: float | None = None


# 🔥 ИНТЕРАКТИВНЫЙ РЕДАКТОР
def interactive_editor(minicards: List[MiniCard] = None) -> List[MiniCard]:
    if minicards is None:
        minicards = []

    while True:
        print("" + "=" * 50)
        print("MINICARD EDITOR")
        print("0. Добавить новую")
        print("1. Редактировать")
        print("2. Удалить")
        print("3. Сохранить JSON")
        print("4. Загрузить JSON")
        print("5. Выход")

        for i, card in enumerate(minicards):
            print(f"{i}. {card.name} - {card.price}₽ [{card.category.value}]")

        choice = input("Выбор: ").strip()

        if choice == "0":
            minicards.append(create_minicard())
        elif choice == "1" and minicards:
            edit_minicard(minicards)
        elif choice == "2" and minicards:
            delete_minicard(minicards)
        elif choice == "3":
            save_json(minicards)
        elif choice == "4":
            minicards = load_json()
        elif choice == "5":
            break

    return minicards


def create_minicard() -> MiniCard:
    print("➕ НОВАЯ MINICARD")
    return MiniCard(
        id=len(load_json() or []) + 1,
        name=input("Название: "),
        price=float(input("Цена: ") or 0),
        size=set(choose_multi("Размеры", Size)),
        category=choose_one("Категория", Category),
        material=choose_one("Материал", Material),
        style=choose_one("Стиль", Style),
        rating=choose_one("Рейтинг", Rating),
        description=input("Описание: ") or "",
        color=int(input("Цвет (ID): ") or 0),
        image="111",
    )


def choose_one(title: str, enum_cls: type[Enum]) -> Enum:
    print(f"{title}:")
    for i, item in enumerate(enum_cls):
        print(f"{i}. {item.value}")
    while True:
        try:
            idx = int(input("Выбери: "))
            return enum_cls(list(enum_cls)[idx])
        except:
            print("Повтори")


def choose_multi(title: str, enum_cls: type[Enum]) -> set:
    print(f"{title} (0=завершить):")
    selected = set()
    for i, item in enumerate(enum_cls):
        print(f"{i}. {item.value}")

    while True:
        idx = input("Выбери (через запятую, 0=готово): ").strip()
        if idx == "0":
            break
        for i in idx.split(","):
            try:
                selected.add(enum_cls(list(enum_cls)[int(i.strip())]))
            except:
                pass
    return selected


def edit_minicard(minicards: List[MiniCard]):
    idx = int(input("Индекс для редактирования: "))
    if 0 <= idx < len(minicards):
        # Перезаполняем все поля
        minicards[idx] = create_minicard()
        minicards[idx].id = idx + 1


def delete_minicard(minicards: List[MiniCard]):
    idx = int(input("Индекс для удаления: "))
    if 0 <= idx < len(minicards):
        del minicards[idx]


# JSON сериализация
def minicard_to_dict(card: MiniCard) -> Dict[str, Any]:
    d = asdict(card)
    d["size"] = [s.value for s in d["size"]]
    d["category"] = card.category.value
    d["material"] = card.material.value
    d["style"] = card.style.value
    d["rating"] = card.rating.value
    return d


def dict_to_minicard(d: Dict[str, Any]) -> MiniCard:
    d = d.copy()
    d["size"] = set(Size(item) for item in d["size"])
    d["category"] = Category(d["category"])
    d["material"] = Material(d["material"])
    d["style"] = Style(d["style"])
    d["rating"] = Rating(d["rating"])
    return MiniCard(**d)


def save_json(minicards: List[MiniCard]):
    data = [minicard_to_dict(c) for c in minicards]
    with open("minicards.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 Сохранено в minicards.json")


def load_json() -> List[MiniCard]:
    try:
        with open(Path(__file__).parent / "mc.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print("Загружено из mc.json")
            return [dict_to_minicard(d) for d in data]
    except FileNotFoundError:
        print("Файл mc.json не найден")
        return []


# 🚀 ЗАПУС


mini_cards: list[MiniCard] = load_json()


@app.get("/")
async def root():
    print("HHHHHHHHHHHHHHHHHHH")


@app.post("/get_minicards")
async def get_minicards(filters: Filters):
    mini_cards: list[MiniCard] = load_json()
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
        print(mini_cards)
        for c in mini_cards:
            c.image = base64.b64encode(get_picture(c.id)).decode("utf-8")
        return list(mini_cards)
    else:
        cards: list[MiniCard] = []
        for card in mini_cards:
            if filters.category and card.category not in filters.category:
                continue
            if filters.size and card.size not in filters.size:
                continue
            if filters.color and card.color not in filters.color:
                print(card)
                continue
            if filters.material and card.material not in filters.material:
                continue
            if filters.style and card.style not in filters.style:
                continue
            if filters.rating and card.rating not in filters.rating:
                continue
            if filters.starting_price and card.price < filters.starting_price:
                continue
            if filters.ending_price and card.price > filters.ending_price:
                continue
            cards.append(card)
            for c in cards:
                c.image = base64.b64encode(get_picture(c.id)).decode("utf-8")

            return cards


def get_id(id: int):
    mini_cards: list[MiniCard] = load_json()
    for card in mini_cards:
        if card.id == id:
            card.image = base64.b64encode(get_picture(card.id)).decode("utf-8")
            return card
    return None


@app.get("/by_id")
async def get_by_id(id: int):
    return get_id(id)
