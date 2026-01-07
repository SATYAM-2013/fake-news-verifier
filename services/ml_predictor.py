from services.transformer_predictor import transformer_predict
from utils.cache import get_ml_cache, set_ml_cache


def predict_news(text: str) -> dict:
    cached = get_ml_cache(text)
    if cached:
        return cached

    result = transformer_predict(text)
    result["text"] = text

    set_ml_cache(text, result)
    return result
