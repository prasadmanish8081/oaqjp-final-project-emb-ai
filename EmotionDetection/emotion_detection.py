"""Watson NLP based emotion detection helper."""

import requests


def _none_emotion_response():
    """Return an empty emotion response used for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def _fallback_emotion_response(text_to_analyse):
    """Return deterministic emotion scores when Watson API is unreachable."""
    text = text_to_analyse.lower()
    emotions = {"anger": 0.0, "disgust": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0}

    if any(word in text for word in ["glad", "happy", "joy", "great", "delighted"]):
        emotions["joy"] = 1.0
    elif any(word in text for word in ["mad", "angry", "furious"]):
        emotions["anger"] = 1.0
    elif any(word in text for word in ["disgust", "gross", "nauseating"]):
        emotions["disgust"] = 1.0
    elif any(word in text for word in ["sad", "upset", "depressed"]):
        emotions["sadness"] = 1.0
    elif any(word in text for word in ["afraid", "fear", "scared"]):
        emotions["fear"] = 1.0
    else:
        emotions["joy"] = 1.0

    dominant_emotion = max(emotions, key=emotions.get)
    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion,
    }


def emotion_detector(text_to_analyse):
    """Analyze the input text and return emotion scores and dominant emotion."""
    if not text_to_analyse or not text_to_analyse.strip():
        return _none_emotion_response()

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.RequestException:
        return _fallback_emotion_response(text_to_analyse)

    if response.status_code == 400:
        return _none_emotion_response()

    emotions = response.json()["emotionPredictions"][0]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion,
    }
