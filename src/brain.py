from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class SentimentBrain:
    def __init__(self):
        print("🧠 Loading FinBERT weights... (This may take a minute on first run)")
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def get_sentiment(self, text: str):
        # 1. Tokenize the input text
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        
        # 2. Perform Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # 3. Convert raw logits to probabilities (0 to 1)
        # FinBERT labels: 0 -> Positive, 1 -> Negative, 2 -> Neutral
        probs = F.softmax(outputs.logits, dim=-1)
        
        # 4. Map to a "Market Sense" score (-1 to 1)
        # We calculate: (Prob Positive - Prob Negative)
        # This gives a clean range where -1 is ultra-bearish and 1 is ultra-bullish
        pos = probs[0][0].item()
        neg = probs[0][1].item()
        neu = probs[0][2].item()
        
        composite_score = pos - neg
        
        # Determine the label
        label = "Neutral"
        if composite_score > 0.15: label = "Bullish"
        if composite_score < -0.15: label = "Bearish"
        
        return {
            "score": round(composite_score, 4),
            "label": label,
            "raw_probs": {"pos": pos, "neg": neg, "neu": neu}
        }

if __name__ == "__main__":
    # Quick Test
    brain = SentimentBrain()
    test_headline = "NVIDIA revenue beats expectations as AI demand surges"
    print(f"Result: {brain.get_sentiment(test_headline)}")