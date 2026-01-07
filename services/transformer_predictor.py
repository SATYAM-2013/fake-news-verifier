from transformers import pipeline

# Load model ONCE at startup (FAANG rule: no reload per request)
_classifier = pipeline(
    task="text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def transformer_predict(text: str) -> dict:
    """
    Transformer-based prediction.
    Output format is normalized for the project:
    {
        label: real | fake | uncertain
        confidence: float (0–1)
    }
    """

    # Safety limit for transformers
    text = text[:512]

    result = _classifier(text)[0]

    label_map = {
        "POSITIVE": "real",
        "NEGATIVE": "fake"
    }

    label = label_map.get(result["label"], "uncertain")
    confidence = round(float(result["score"]), 2)

    return {
        "label": label,
        "confidence": confidence
    }
