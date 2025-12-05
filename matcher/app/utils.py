import torch

def find_closest(image_embedding, catalog_path="./embeddings/catalog_embeddings.pt"):
    data = torch.load(catalog_path)
    catalog_embs = data["embeddings"]
    filenames = data["filenames"]
    
    sims = (catalog_embs @ image_embedding.T).squeeze(1)
    best_idx = sims.argmax().item()
    return filenames[best_idx], sims[best_idx].item()

