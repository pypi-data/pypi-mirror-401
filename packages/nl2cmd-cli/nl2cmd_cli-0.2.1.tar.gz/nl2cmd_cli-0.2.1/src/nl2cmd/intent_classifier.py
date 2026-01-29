import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class IntentClassifier:
    def __init__(self, dataset_path="training/data/intent_dataset.json"):
        # Load pretrained sentence transformer
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load intent dataset
        with open(dataset_path, "r") as f:
            data = json.load(f)

        self.intent_texts = {}
        for item in data:
            self.intent_texts.setdefault(item["intent"], []).append(item["input"])

        # Precompute embeddings for each intent
        self.intent_embeddings = {}
        for intent, texts in self.intent_texts.items():
            embeddings = self.model.encode(texts)
            self.intent_embeddings[intent] = np.mean(embeddings, axis=0)

    def predict_intent(self, text):
        query_embedding = self.model.encode([text])[0]

        best_intent = "UNKNOWN"
        best_score = 0.0

        for intent, emb in self.intent_embeddings.items():
            score = cosine_similarity(
                [query_embedding], [emb]
            )[0][0]

            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent, float(best_score)
