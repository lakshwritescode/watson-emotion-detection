# IBM Watson NLP Emotion Detection Web Application

An end-to-end Python Flask web application that performs sentiment and emotion analysis using the IBM Watson NLP EmotionPredict service. The application classifies English text across five emotional dimensions—**anger**, **disgust**, **fear**, **joy**, and **sadness**—identifying the dominant emotion and presenting the findings through both a web interface and an API endpoint.

This repository fulfills **Tasks 2 through 8** of the IBM Applied AI / AI Developer coursework assignment.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Coursework Task Breakdown](#coursework-task-breakdown)
   - [Task 2: Application Creation](#task-2-application-creation)
   - [Task 3: Formatted Output](#task-3-formatted-output)
   - [Task 4: Package Packaging & Validation](#task-4-package-packaging--validation)
   - [Task 5: Unit Testing](#task-5-unit-testing)
   - [Task 6: Flask Web Deployment](#task-6-flask-web-deployment)
   - [Task 7: Robust Error Handling](#task-7-robust-error-handling)
   - [Task 8: Static Code Analysis (Pylint 10/10)](#task-8-static-code-analysis-pylint-1010)
5. [Prerequisites & Installation](#prerequisites--installation)
6. [How to Run the Application](#how-to-run-the-application)
7. [How to Run Unit Tests](#how-to-run-unit-tests)
8. [How to Run Pylint](#how-to-run-pylint)
9. [API Route Reference](#api-route-reference)
10. [IBM Watson Endpoint Architecture & Network Notes](#ibm-watson-endpoint-architecture--network-notes)
11. [Evidence and Screenshot Index](#evidence-and-screenshot-index)
12. [Git Repository Details](#git-repository-details)

---

## Project Overview

The Emotion Detection system accepts natural language text, interacts with the IBM Watson NLP runtime service via RESTful API calls, and processes the response into an accessible format:
- Evaluates individual confidence scores for five primary emotions: `anger`, `disgust`, `fear`, `joy`, `sadness`.
- Identifies the `dominant_emotion` corresponding to the highest confidence score.
- Returns the exact system response string required by the IBM evaluation rubric.
- Handles empty queries, whitespace inputs, HTTP 400 errors, and network timeouts safely.

---

## Technology Stack

- **Python**: Core programming language.
- **Flask**: Lightweight WSGI web framework for serving the interface and endpoints.
- **IBM Watson NLP EmotionPredict API**: Aggregated emotion classification model (`emotion_aggregated-workflow_lang_en_stock`).
- **Requests**: HTTP client for interacting with the Watson NLP service.
- **HTML5, CSS3, Vanilla JavaScript**: Modern, responsive, dependency-free frontend.
- **unittest**: Python standard library unit testing framework.
- **Pylint**: Static code analysis and PEP 8 compliance tool.

---

## Project Structure

```text
emotionFlask/
├── EmotionDetection/
│   ├── __init__.py                 # Package initializer exporting emotion_detector
│   └── emotion_detection.py        # Watson NLP API integration and score computation
├── test_emotion_detection.py       # Deterministic unit test suite with mocked requests
├── server.py                       # Flask application with routes '/' and '/emotionDetector'
├── templates/
│   └── index.html                  # Responsive HTML user interface
├── static/
│   ├── style.css                   # Custom styling and color palette
│   └── script.js                   # Client-side request handler and DOM updater
├── requirements.txt                # Python project dependencies
├── README.md                       # Comprehensive documentation
└── screenshots/
    ├── 2b_application_creation.png      # Task 2: Function creation and initial execution
    ├── 3b_output_format.png             # Task 3: Output dictionary with 6 keys
    ├── 4b_package_validation.png        # Task 4: Package import validation
    ├── 5b_unit_tests.png                # Task 5: 12/12 unit tests passing
    ├── 6b_deployment_test.png           # Task 6: Browser deployment test
    ├── 7c_error_handling_interface.png  # Task 7: Blank input error handling
    └── 8a_static_analysis.png           # Task 8: Pylint static analysis (10.00/10)
```

---

## Coursework Task Breakdown

### Task 2: Application Creation
The `emotion_detector(text_to_analyze)` function in `EmotionDetection/emotion_detection.py` connects to the IBM Watson NLP runtime service:
- **Endpoint**: `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`
- **Header**: `{"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}`
- **Payload**: `{"raw_document": {"text": text_to_analyze}}`

### Task 3: Formatted Output
The function parses the API's JSON response and returns a dictionary with exactly six keys:
```python
{
    "anger": 0.0052,
    "disgust": 0.0031,
    "fear": 0.0074,
    "joy": 0.9581,
    "sadness": 0.0123,
    "dominant_emotion": "joy"
}
```
The `dominant_emotion` is dynamically selected using `max()` over the emotional scores.

### Task 4: Package Packaging & Validation
`EmotionDetection/__init__.py` exposes the module function at the package level:
```python
from .emotion_detection import emotion_detector
```
Both of the following import styles resolve cleanly:
```python
from EmotionDetection import emotion_detector
from EmotionDetection.emotion_detection import emotion_detector
```

### Task 5: Unit Testing
The `test_emotion_detection.py` test suite covers 12 test cases using `unittest` and `unittest.mock`:
- Individual tests verifying joy, anger, disgust, sadness, and fear classification.
- Output dictionary structure and 6-key presence checks.
- Verification that `dominant_emotion` matches the maximum score.
- HTTP 400 error status code handling.
- Blank and whitespace input validation.
- Connection timeout and HTTP 500 error resilience.
- Malformed JSON recovery.

### Task 6: Flask Web Deployment
`server.py` exposes:
- `GET /`: Renders `templates/index.html`.
- `GET /emotionDetector?textToAnalyze=<text>`: Calls `emotion_detector()` and returns the formatted response string:
  > *"For the given statement, the system response is 'anger': 0.0048, 'disgust': 0.0031, 'fear': 0.0052, 'joy': 0.9624 and 'sadness': 0.0118. The dominant emotion is joy."*

### Task 7: Robust Error Handling
- **API 400 or Network Failures**: `emotion_detector()` returns `{ 'anger': None, 'disgust': None, 'fear': None, 'joy': None, 'sadness': None, 'dominant_emotion': None }`.
- **Blank / Whitespace Queries**: Checked in both `server.py` and `static/script.js`, displaying:
  > `"Invalid text! Please try again!"`
  No blank requests are dispatched to the external API.

### Task 8: Static Code Analysis (Pylint 10/10)
Both `server.py` and `EmotionDetection/emotion_detection.py` conform to PEP 8 standards and achieve a **10.00/10 score** under Pylint:
```text
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

---

## Prerequisites & Installation

### 1. Clone or Open the Project
Navigate to the project root directory:
```bash
cd emotionFlask
```

### 2. Set Up a Virtual Environment (Recommended)
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run the Application

Start the Flask development server on port 5000:

**Windows PowerShell:**
```powershell
python server.py
```

**macOS / Linux:**
```bash
python3 server.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

Type a statement such as `"I think I am having fun"` and click **Analyze Emotion**.

---

## How to Run Unit Tests

Execute the unit test suite offline without requiring external internet or API connectivity:

**Windows PowerShell:**
```powershell
python -m unittest -v test_emotion_detection.py
```

**macOS / Linux:**
```bash
python3 -m unittest -v test_emotion_detection.py
```

Expected output:
```text
test_anger_detection (test_emotion_detection.TestEmotionDetection.test_anger_detection) ... ok
test_api_500_server_error (test_emotion_detection.TestEmotionDetection.test_api_500_server_error) ... ok
test_api_timeout_handling (test_emotion_detection.TestEmotionDetection.test_api_timeout_handling) ... ok
test_blank_and_whitespace_input (test_emotion_detection.TestEmotionDetection.test_blank_and_whitespace_input) ... ok
test_disgust_detection (test_emotion_detection.TestEmotionDetection.test_disgust_detection) ... ok
test_dominant_emotion_matches_highest_score (test_emotion_detection.TestEmotionDetection.test_dominant_emotion_matches_highest_score) ... ok
test_fear_detection (test_emotion_detection.TestEmotionDetection.test_fear_detection) ... ok
test_http_400_response (test_emotion_detection.TestEmotionDetection.test_http_400_response) ... ok
test_joy_detection (test_emotion_detection.TestEmotionDetection.test_joy_detection) ... ok
test_malformed_json_response (test_emotion_detection.TestEmotionDetection.test_malformed_json_response) ... ok
test_output_dictionary_keys (test_emotion_detection.TestEmotionDetection.test_output_dictionary_keys) ... ok
test_sadness_detection (test_emotion_detection.TestEmotionDetection.test_sadness_detection) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.007s

OK
```

---

## How to Run Pylint

Analyze code quality across all modules:

**Analyze `server.py`:**
```bash
python -m pylint server.py
```
*Result: 10.00/10*

**Analyze `EmotionDetection/emotion_detection.py`:**
```bash
python -m pylint EmotionDetection/emotion_detection.py
```
*Result: 10.00/10*

---

## API Route Reference

### `GET /`
- **Description**: Serves the main HTML single-page interface.
- **Response**: `200 OK` (HTML document).

### `GET /emotionDetector`
- **Description**: Evaluates text sentiment.
- **Parameters**: `textToAnalyze` (string, query parameter).
- **Valid Request**:
  ```text
  GET /emotionDetector?textToAnalyze=I%20think%20I%20am%20having%20fun
  ```
  **Response**:
  ```text
  For the given statement, the system response is 'anger': 0.0048, 'disgust': 0.0031, 'fear': 0.0052, 'joy': 0.9624 and 'sadness': 0.0118. The dominant emotion is joy.
  ```
- **Invalid / Blank Request**:
  ```text
  GET /emotionDetector?textToAnalyze=
  ```
  **Response**:
  ```text
  Invalid text! Please try again!
  ```

---

## IBM Watson Endpoint Architecture & Network Notes

> [!NOTE]
> The domain `sn-watson-emotion.labs.skills.network` is an IBM internal educational service endpoint. DNS resolution points to private RFC 1918 IP addresses (`10.241.65.62` and `10.241.1.96`).
>
> - **Inside IBM Skills Network Cloud IDE**: Requests route directly to the Watson microservice container on the IBM private VPC network.
> - **Outside IBM Cloud (Local Workstations)**: Connections to `10.241.x.x` will experience a connection timeout.
>
> To ensure flawless development in both environments:
> 1. `emotion_detector()` gracefully catches `requests.exceptions.RequestException` and timeouts, returning the required `None` format without crashing.
> 2. The unit test suite uses `unittest.mock` to guarantee 100% test reliability anywhere.
> 3. An optional environment variable `WATSON_EMOTION_URL` can be specified to point to a local proxy or mock service for offline end-to-end integration testing.

---

## Evidence and Screenshot Index

All required screenshots are stored in the `screenshots/` directory:

| Filename | Assignment Task | Description |
| :--- | :--- | :--- |
| `2b_application_creation.png` | Task 2 | Terminal execution of `emotion_detector("I love this new technology")` |
| `3b_output_format.png` | Task 3 | Terminal validation of the 6-key dictionary format and dominant emotion |
| `4b_package_validation.png` | Task 4 | Import verification of `from EmotionDetection import emotion_detector` |
| `5b_unit_tests.png` | Task 5 | Terminal output of 12 unit tests passing (`python -m unittest -v`) |
| `6b_deployment_test.png` | Task 6 | Browser view of the running Flask app analyzing `"I think I am having fun"` |
| `7c_error_handling_interface.png` | Task 7 | Browser view demonstrating `"Invalid text! Please try again!"` on blank input |
| `8a_static_analysis.png` | Task 8 | Terminal output showing `pylint server.py` rated **10.00/10** |

---

## Git Repository Details

When pushing to your GitHub account:

1. Initialize git and commit:
   ```bash
   git init
   git add .
   git commit -m "Complete IBM Watson NLP Emotion Detection coursework tasks 2-8"
   ```
2. Link your remote repository and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git branch -M main
   git push -u origin main
   ```
3. Submission URL template for Task 4:
   ```text
   https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/EmotionDetection/__init__.py
   ```

