_classifier = None

def ml_translate(text: str):
    global _classifier

    if _classifier is None:
        from nl2cmd.intent_classifier import IntentClassifier
        _classifier = IntentClassifier()

    intent, score = _classifier.predict_intent(text)

    if score < 0.55:
        print(f"[ML] Low confidence ({score:.2f}), intent UNKNOWN")
        return "INTENT=UNKNOWN"

    print(f"[ML] Predicted intent: {intent} (confidence={score:.2f})")
    return f"INTENT={intent}"
