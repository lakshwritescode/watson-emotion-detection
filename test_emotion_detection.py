"""Unit tests for the EmotionDetection package.

Tests the emotion_detector function using mocked IBM Watson NLP responses
to ensure deterministic, offline execution and high test coverage.
"""

import unittest
from unittest.mock import Mock, patch
import requests

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Test suite for emotion detection logic, output format, and error handling."""

    def _create_mock_response(self, emotions, status_code=200):
        """Helper to create a mock requests.Response object."""
        mock_resp = Mock()
        mock_resp.status_code = status_code
        if status_code == 200:
            mock_resp.json.return_value = {
                "emotionPredictions": [
                    {
                        "emotion": emotions
                    }
                ]
            }
        else:
            mock_resp.json.return_value = {"error": "Invalid request"}
        return mock_resp

    @patch("requests.post")
    def test_joy_detection(self, mock_post):
        """Test that statement with highest joy score identifies joy as dominant."""
        emotions = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.01,
            "joy": 0.95,
            "sadness": 0.01,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I am glad this happened")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.95)

    @patch("requests.post")
    def test_anger_detection(self, mock_post):
        """Test that statement with highest anger score identifies anger as dominant."""
        emotions = {
            "anger": 0.91,
            "disgust": 0.03,
            "fear": 0.02,
            "joy": 0.01,
            "sadness": 0.03,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I am really mad about this")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertEqual(result["anger"], 0.91)

    @patch("requests.post")
    def test_disgust_detection(self, mock_post):
        """Test that statement with highest disgust identifies disgust as dominant."""
        emotions = {
            "anger": 0.02,
            "disgust": 0.88,
            "fear": 0.03,
            "joy": 0.02,
            "sadness": 0.05,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dominant_emotion"], "disgust")
        self.assertEqual(result["disgust"], 0.88)

    @patch("requests.post")
    def test_sadness_detection(self, mock_post):
        """Test that statement with highest sadness identifies sadness as dominant."""
        emotions = {
            "anger": 0.03,
            "disgust": 0.02,
            "fear": 0.04,
            "joy": 0.01,
            "sadness": 0.90,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I am so sad about this")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dominant_emotion"], "sadness")
        self.assertEqual(result["sadness"], 0.90)

    @patch("requests.post")
    def test_fear_detection(self, mock_post):
        """Test that statement with highest fear score identifies fear as dominant."""
        emotions = {
            "anger": 0.04,
            "disgust": 0.01,
            "fear": 0.89,
            "joy": 0.01,
            "sadness": 0.05,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I am really afraid that this will happen")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dominant_emotion"], "fear")
        self.assertEqual(result["fear"], 0.89)

    @patch("requests.post")
    def test_output_dictionary_keys(self, mock_post):
        """Verify output dictionary contains exactly all six required keys."""
        emotions = {
            "anger": 0.1,
            "disgust": 0.1,
            "fear": 0.1,
            "joy": 0.6,
            "sadness": 0.1,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I think I am having fun")
        expected_keys = {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}
        self.assertEqual(set(result.keys()), expected_keys)

    @patch("requests.post")
    def test_dominant_emotion_matches_highest_score(self, mock_post):
        """Verify dominant emotion always matches the emotion with the maximum score."""
        emotions = {
            "anger": 0.15,
            "disgust": 0.05,
            "fear": 0.10,
            "joy": 0.65,
            "sadness": 0.05,
        }
        mock_post.return_value = self._create_mock_response(emotions)

        result = emotion_detector("I think I am having fun")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result[result["dominant_emotion"]], 0.65)

    @patch("requests.post")
    def test_http_400_response(self, mock_post):
        """Verify that an HTTP 400 response from the API returns all None values."""
        mock_post.return_value = self._create_mock_response({}, status_code=400)

        result = emotion_detector("Some bad input triggering 400")
        for key in ["anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"]:
            self.assertIsNone(result[key])

    def test_blank_and_whitespace_input(self):
        """Verify that empty or whitespace strings return all None values without API call."""
        blank_cases = ["", "   ", "\t\n", None]
        for case in blank_cases:
            result = emotion_detector(case)
            self.assertIsInstance(result, dict)
            for key in ["anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"]:
                self.assertIsNone(result[key], f"Key {key} was not None for input {case!r}")

    @patch("requests.post")
    def test_api_timeout_handling(self, mock_post):
        """Verify that connection timeout does not crash and returns all None values."""
        mock_post.side_effect = requests.exceptions.ConnectTimeout("Connection timed out")

        result = emotion_detector("Test timeout scenario")
        self.assertIsInstance(result, dict)
        self.assertIsNone(result["dominant_emotion"])
        self.assertIsNone(result["joy"])

    @patch("requests.post")
    def test_api_500_server_error(self, mock_post):
        """Verify that HTTP 500 error returns all None values safely."""
        mock_post.return_value = self._create_mock_response({}, status_code=500)

        result = emotion_detector("Test 500 scenario")
        self.assertIsNone(result["dominant_emotion"])

    @patch("requests.post")
    def test_malformed_json_response(self, mock_post):
        """Verify that malformed JSON from API is caught safely and returns None."""
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"unexpected_format": True}
        mock_post.return_value = mock_resp

        result = emotion_detector("Test malformed scenario")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()

