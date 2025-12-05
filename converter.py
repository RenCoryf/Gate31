import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from main import Category, Material, MiniCard, Rating, Size, Style


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
        with open("minicards.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [dict_to_minicard(d) for d in data]
    except FileNotFoundError:
        return []


# 🚀 ЗАПУСК
if __name__ == "__main__":
    cards = interactive_editor()
    print(f"✅ Готово! {len(cards)} карточек.")
    print(cards)
