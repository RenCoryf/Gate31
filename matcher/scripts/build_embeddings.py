import torch
from PIL import Image
from pathlib import Path
from matcher.app.embedder import get_embedding

catalog_dir = Path(__file__).resolve().parent.parent.parent / "catalog"
embeddings_dir = Path(__file__).resolve().parent.parent / "embeddings"
embeddings_dir.mkdir(exist_ok=True)

embeddings = []
filenames = []

print("Начинаем обработку каталога...")

for file in catalog_dir.glob("*.*"):  # все картинки
    try:
        img = Image.open(file)
        emb = get_embedding(img)
        embeddings.append(emb)
        filenames.append(file.name)
        print(f"Processed {file.name}")
    except Exception as e:
        print(f"Failed to process {file.name}: {e}")

if not embeddings:
    raise ValueError("Не удалось обработать ни одной картинки! Проверь каталог и формат файлов.")

torch.save(
    {"embeddings": torch.cat(embeddings), "filenames": filenames},
    embeddings_dir / "catalog_embeddings.pt"
)

print(f"Готово! {len(filenames)} эмбеддингов сохранено в {embeddings_dir}/catalog_embeddings.pt")

