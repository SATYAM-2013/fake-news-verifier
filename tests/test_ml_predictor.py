from services.ml_predictor import predict_news

def test_predict_returns_label():
    result = predict_news("WHO confirms vaccines are safe")
    assert "label" in result
    assert "confidence" in result

def test_predict_confidence_range():
    result = predict_news("random sentence")
    assert 0 <= result["confidence"] <= 1
