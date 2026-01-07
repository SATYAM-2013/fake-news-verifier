# utils/history.py
from datetime import datetime

_history = []

def add_history(claim, verdict):
    _history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "claim": claim[:80] + ("..." if len(claim) > 80 else ""),
        "verdict": verdict
    })

def get_history(limit=5):
    return _history[-limit:]
