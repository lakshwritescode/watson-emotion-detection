"""Flask server implementation for the Emotion Detection application.

Provides routes for serving the front-end user interface and processing
emotion analysis requests via the EmotionDetection package.
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/")
def render_index_page():
    """Render the primary HTML user interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Process emotion detection requests and return formatted response string."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    # Validate that input is neither None nor blank whitespace
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    # Call emotion detection service
    response = emotion_detector(text_to_analyze)
    dominant_emotion = response.get("dominant_emotion")

    # If Watson API returned error or dominant emotion is absent
    if dominant_emotion is None:
        return "Invalid text! Please try again!"

    # Format output according to coursework specifications
    return (
        f"For the given statement, the system response is 'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
        f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
        f"The dominant emotion is {dominant_emotion}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

