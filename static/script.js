/**
 * IBM Watson NLP Emotion Detection - Client Application
 */

function runEmotionAnalysis() {
    const textInput = document.getElementById("textToAnalyze");
    const textToAnalyze = textInput.value;
    const errorContainer = document.getElementById("error-container");
    const errorText = document.getElementById("error-text");
    const resultsContainer = document.getElementById("results-container");
    const systemResponse = document.getElementById("system_response");
    const submitBtn = document.getElementById("submit-btn");
    const spinner = document.getElementById("loading-spinner");
    const btnText = submitBtn.querySelector(".btn-text");

    // Clear previous state
    errorContainer.classList.add("hidden");
    resultsContainer.classList.add("hidden");

    // Client-side validation: reject empty or whitespace-only inputs
    if (!textToAnalyze || !textToAnalyze.trim()) {
        errorText.textContent = "Invalid text! Please try again!";
        errorContainer.classList.remove("hidden");
        return;
    }

    // Set UI to loading state
    submitBtn.disabled = true;
    spinner.classList.remove("hidden");
    btnText.textContent = "Analyzing...";

    const url = `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`;

    fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }
            return response.text();
        })
        .then((data) => {
            // Restore button state
            submitBtn.disabled = false;
            spinner.classList.add("hidden");
            btnText.textContent = "Analyze Emotion";

            const trimmedData = data.trim();

            // Check if server returned the invalid text error string
            if (trimmedData === "Invalid text! Please try again!") {
                errorText.textContent = trimmedData;
                errorContainer.classList.remove("hidden");
                return;
            }

            // Populate official system response container
            systemResponse.textContent = trimmedData;

            // Extract scores and dominant emotion using regex from the formatted string:
            // "For the given statement, the system response is 'anger': 0.01, 'disgust': 0.02, 'fear': 0.03, 'joy': 0.94 and 'sadness': 0.01. The dominant emotion is joy."
            const dominantMatch = trimmedData.match(/The dominant emotion is\s+([a-zA-Z]+)\.?/i);
            const angerMatch = trimmedData.match(/'anger':\s*([0-9.]+)/i);
            const disgustMatch = trimmedData.match(/'disgust':\s*([0-9.]+)/i);
            const fearMatch = trimmedData.match(/'fear':\s*([0-9.]+)/i);
            const joyMatch = trimmedData.match(/'joy':\s*([0-9.]+)/i);
            const sadnessMatch = trimmedData.match(/'sadness':\s*([0-9.]+)/i);

            if (dominantMatch) {
                const dominant = dominantMatch[1];
                document.getElementById("dominant-emotion-text").textContent = dominant;
            }

            const updateScore = (name, match) => {
                const score = match ? parseFloat(match[1]) : 0;
                const scoreElem = document.getElementById(`score-${name}`);
                const barElem = document.getElementById(`bar-${name}`);
                if (scoreElem) scoreElem.textContent = score.toFixed(4);
                if (barElem) barElem.style.width = `${Math.min(100, Math.max(0, score * 100))}%`;
            };

            updateScore("joy", joyMatch);
            updateScore("sadness", sadnessMatch);
            updateScore("anger", angerMatch);
            updateScore("fear", fearMatch);
            updateScore("disgust", disgustMatch);

            // Display results container
            resultsContainer.classList.remove("hidden");
        })
        .catch((error) => {
            submitBtn.disabled = false;
            spinner.classList.add("hidden");
            btnText.textContent = "Analyze Emotion";

            errorText.textContent = "An error occurred while contacting the server. Please try again!";
            errorContainer.classList.remove("hidden");
            console.error("Emotion analysis request failed:", error);
        });
}

function clearInput() {
    document.getElementById("textToAnalyze").value = "";
    document.getElementById("error-container").classList.add("hidden");
    document.getElementById("results-container").classList.add("hidden");
}

// Allow Ctrl+Enter or Cmd+Enter to submit
document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("textToAnalyze");
    if (textarea) {
        textarea.addEventListener("keydown", (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                e.preventDefault();
                runEmotionAnalysis();
            }
        });
    }
});

