import random

class EmbeddingService:
    
    def generate(self, text: str) -> list:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]
