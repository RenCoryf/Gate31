from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from PIL import Image
import torch
from matcher.app.embedder import get_embedding

router = APIRouter()

# Загружаем эмбеддинги каталога один раз при старте сервера
embeddings_file = Path(__file__).resolve().parent.parent / "embeddings/catalog_embeddings.pt"
if not embeddings_file.exists():
    raise FileNotFoundError(f"Эмбеддинги каталога не найдены: {embeddings_file}")

data = torch.load(embeddings_file)
catalog_embeddings = data["embeddings"]
catalog_filenames = data["filenames"]

@router.post("/match")
async def match(file: UploadFile = File(...)):
    # Проверка формата
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
    
    try:
        # Загружаем изображение
        img = Image.open(file.file)
        emb = get_embedding(img)  # Получаем эмбеддинг
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Не удалось обработать изображение: {e}")
    
    # Считаем косинусное сходство с каталогом
    sims = (catalog_embeddings @ emb.T).squeeze(1)  # [num_catalog]
    best_idx = sims.argmax().item()
    best_score = sims[best_idx].item()
    
    return JSONResponse({"match": catalog_filenames[best_idx], "score": round(best_score, 3)})

