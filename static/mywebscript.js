function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const endpoint = `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`;

    fetch(endpoint)
        .then((response) => response.text())
        .then((result) => {
            document.getElementById("system_response").innerHTML = result;
        })
        .catch(() => {
            document.getElementById("system_response").innerHTML =
                "Unable to process request.";
        });
}

