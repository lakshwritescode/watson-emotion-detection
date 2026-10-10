"""Emotion Detection module using IBM Watson NLP EmotionPredict service.

This module provides the emotion_detector function, which sends text to the
Watson NLP EmotionPredict API and returns the confidence scores for anger,
disgust, fear, joy, and sadness, along with the dominant emotion.
"""

import os
import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def emotion_detector(text_to_analyze):
    """Analyze the emotion of the given text using IBM Watson NLP.

    Args:
        text_to_analyze (str): Text string to analyze for emotional sentiment.

    Returns:
        dict: A dictionary containing scores for anger, disgust, fear, joy,
              and sadness, plus the dominant_emotion. Returns None for all
              keys if the input is blank or if the API returns an error.
    """
    error_response = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

    # Handle blank or whitespace-only input
    if not text_to_analyze or not str(text_to_analyze).strip():
        return error_response

    target_url = os.environ.get("WATSON_EMOTION_URL", WATSON_URL)
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            target_url,
            headers=HEADERS,
            json=payload,
            timeout=10,
        )

        # Handle 400 Bad Request error status from Watson API
        if response.status_code == 400 or response.status_code != 200:
            return error_response

        # Parse JSON response
        formatted_response = response.json()
        emotions = formatted_response["emotionPredictions"][0]["emotion"]

        dominant_emotion = max(
            ["anger", "disgust", "fear", "joy", "sadness"],
            key=lambda key: emotions.get(key, 0),
        )

        return {
            "anger": emotions.get("anger"),
            "disgust": emotions.get("disgust"),
            "fear": emotions.get("fear"),
            "joy": emotions.get("joy"),
            "sadness": emotions.get("sadness"),
            "dominant_emotion": dominant_emotion,
        }

    except (requests.exceptions.RequestException, KeyError, IndexError, TypeError, ValueError):
        return error_response

