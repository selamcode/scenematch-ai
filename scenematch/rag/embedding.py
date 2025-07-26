from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import Document
from scenematch.util import load_json
from typing import List


EMB_MODEL = "jinaai/jina-embeddings-v2-small-en"   

def prepare_points(docs: List[dict]) -> List[PointStruct]:
    points: List[PointStruct] = []

    for doc in docs:
        # Raw text
        overview: str  = doc.get("overview", "")
        tagline: str   = doc.get("tagline", "")
        genres         = doc.get("genres", [])
        keywords       = doc.get("keywords", [])
        cast           = doc.get("cast", [])       
        director: str  = doc.get("director", "")

        # Normalise lists 
        genres_list   = [str(g) for g in (genres   if isinstance(genres,  list) else [genres])   if g]
        keywords_list = [str(k) for k in (keywords if isinstance(keywords, list) else [keywords]) if k]
        cast_list     = [str(c) for c in (cast     if isinstance(cast,     list) else [cast])     if c]

        # Join helper strings
        text_genres    = " ".join(genres_list)
        text_keywords  = " ".join(keywords_list)
        text_cast      = " ".join(cast_list)
        text_names_all = f"{text_cast} {director}".strip()

        # Vectors
        vectors = {
            # Dense semantic
            "overview_dense":  Document(text=overview,   model=EMB_MODEL),
            "tagline_dense":   Document(text=tagline,    model=EMB_MODEL),
            "keywords_dense":  Document(text=text_keywords, model=EMB_MODEL),
            "cast_dense":      Document(text=text_cast,  model=EMB_MODEL),
            "director_dense":  Document(text=director,   model=EMB_MODEL),

            # Sparse BM25
            "overview_sparse_bm25":  Document(text=overview,        model="Qdrant/bm25"),
            "genre_sparse_bm25":     Document(text=text_genres,     model="Qdrant/bm25"),
            "keywords_sparse_bm25":  Document(text=text_keywords,   model="Qdrant/bm25"),
            "names_sparse_bm25":     Document(text=text_names_all,  model="Qdrant/bm25"),
        }

        # Payload (for filtering / reranking)
        payload = {
            "uuid":      doc.get("uuid"),
            "title":     doc.get("title"),
            "overview":  overview,
            "tagline":   tagline,
            "genres":    genres_list,
            "keywords":  keywords_list,
            "cast":      cast_list,
            "director":  director,
            "vote_average": doc.get("vote_average"),
            "release_year": (doc.get("release_date") or "")[:4],
            "runtime":   doc.get("runtime"),
            "language":  doc.get("original_language"),
            "popularity": doc.get("popularity"),
        }

        points.append(
            PointStruct(
                id=doc["id"],
                vector=vectors,
                payload=payload,
            )
        )

    return points


def upsert_points(client: QdrantClient, collection_name: str, points: list[PointStruct], batch_size: int = 300) -> None:
    total = len(points)
    print(f"Starting to insert {total} points into '{collection_name}' in batches of {batch_size}...")

    for i in range(0, total, batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch,
        )
        print(f"✅ Inserted batch {i // batch_size + 1} — Total so far: {i + len(batch)} / {total}")

    print(f"🎉 Finished inserting all {total} points into '{collection_name}'.")


def embed(collection_name: str, json_file: str, client: QdrantClient) -> None:
    docs = load_json(json_file)
    points = prepare_points(docs)
    upsert_points(client, collection_name, points)
