from typing import Dict

_ml_cache: Dict[str, dict] = {}
_fact_cache: Dict[str, dict] = {}
_llm_cache: Dict[str, str] = {}


def get_ml_cache(text: str):
    return _ml_cache.get(text)


def set_ml_cache(text: str, result: dict):
    _ml_cache[text] = result


def get_fact_cache(text: str):
    return _fact_cache.get(text)


def set_fact_cache(text: str, result: dict):
    _fact_cache[text] = result


def get_llm_cache(key: str):
    return _llm_cache.get(key)


def set_llm_cache(key: str, value: str):
    _llm_cache[key] = value
