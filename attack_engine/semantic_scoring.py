from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_score(text, intents):
    emb_text = model.encode([text])
    emb_intents = model.encode(intents)
    sims = cosine_similarity(emb_text, emb_intents)[0]
    return float(max(sims))
