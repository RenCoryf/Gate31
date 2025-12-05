import os
from pathlib import Path


def get_picture(pic_id: int) -> bytes:
    os.chdir(Path(__file__).parent / "catalog")
    files = [f for f in os.listdir(".") if f.lower().endswith(".jpg")]
    files.sort()  # Сортируем, чтобы порядок был предсказуемый

    if pic_id < 1 or pic_id > len(files):
        raise IndexError("Такого номера картинки нет.")

    filename = files[pic_id - 1]
    with open(filename, "rb") as f:
        return f.read()


print(get_picture(2))
