from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# =====================================================
# MODEL PATHS
# =====================================================
SHORT_MODEL_PATH = "fine_tuned_model"
FULL_MODEL_PATH = "full_text_model"

# =====================================================
# LOAD MODELS
# =====================================================
short_tokenizer = AutoTokenizer.from_pretrained(SHORT_MODEL_PATH)
short_model = AutoModelForSequenceClassification.from_pretrained(SHORT_MODEL_PATH)

full_tokenizer = AutoTokenizer.from_pretrained(FULL_MODEL_PATH)
full_model = AutoModelForSequenceClassification.from_pretrained(FULL_MODEL_PATH)

device = 0 if torch.cuda.is_available() else -1

short_classifier = pipeline(
    "text-classification",
    model=short_model,
    tokenizer=short_tokenizer,
    device=device,
    top_k=None
)

full_classifier = pipeline(
    "text-classification",
    model=full_model,
    tokenizer=full_tokenizer,
    device=device,
    top_k=None
)

print("Label mapping:", short_model.config.id2label)
print("✅ Dual-model Transformer loaded successfully")

# =====================================================
# PREDICTION LOGIC
# =====================================================
def predict_news(text: str):
    word_count = len(text.split())

    # Warning for very short scientific claims
    if word_count < 6 and "found" in text.lower():
        print("⚠️ Very short scientific claim — prediction may be unreliable")

    # Guard: too short to classify
    if word_count < 3:
        return {
            "label": "NOT_NEWS",
            "confidence": 0.0,
            "model": "None"
        }

    # Model routing
    if word_count <= 25:
        scores = short_classifier(text)[0]
        model_used = "Short-text model"
    else:
        scores = full_classifier(text)[0]
        model_used = "Full-text model"

    label_scores = {item["label"]: item["score"] for item in scores}

    fake_score = label_scores.get("FAKE", 0.0)
    real_score = label_scores.get("REAL", 0.0)

    # ---------------- UNVERIFIABLE ZONE ----------------
    if fake_score < 0.55 and real_score < 0.55:
        return {
            "label": "UNVERIFIABLE",
            "confidence": max(fake_score, real_score),
            "model": model_used
        }

    # Trusted scientific source override
    trusted_sources = ["nasa", "who", "isro", "esa", "mit", "harvard"]
    if any(src in text.lower() for src in trusted_sources):
        if real_score > 0.35:
            return {
                "label": "REAL",
                "confidence": real_score,
                "model": model_used + " + source-check"
            }

    # Margin-based decision
    if fake_score - real_score > 0.2:
        return {
            "label": "FAKE",
            "confidence": fake_score,
            "model": model_used
        }

    if real_score - fake_score > 0.2:
        return {
            "label": "REAL",
            "confidence": real_score,
            "model": model_used
        }

    # Fallback: uncertain
    return {
        "label": "UNCERTAIN",
        "confidence": max(fake_score, real_score),
        "model": model_used
    }

# =====================================================
# INTERACTIVE LOOP
# =====================================================
while True:
    text = input("\nEnter news text (or type exit): ").strip()
    if text.lower() == "exit":
        break

    result = predict_news(text)

    print(f"[INFO] Model used: {result['model']}")

    if result["label"] == "NOT_NEWS":
        print("⚠️ Input does not look like a valid news headline/article.")
        continue

    if result["label"] == "UNCERTAIN":
        print("🟡 UNCERTAIN")
        print(f"Confidence: {result['confidence'] * 100:.2f}%")
        continue

    if result["label"] == "UNVERIFIABLE":
        print("🔍 UNVERIFIABLE NEWS")
        print("⚠️ Model cannot confidently classify this news")
        print(f"Confidence: {result['confidence'] * 100:.2f}%")
        continue

    emoji = "❌" if result["label"] == "FAKE" else "✅"
    print(f"{emoji} {result['label']} NEWS")
    print(f"Confidence: {result['confidence'] * 100:.2f}%")
