console.log("BACKGROUND SERVICE WORKER STARTED");

// LISTEN FOR MESSAGES FROM CONTENT.JS
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("MESSAGE ARRIVED:", message);
    if (message.type === "ANALYZE_TEXT") {
        const text = message.text;
        console.log("Received from content.js:", text);
        // Send to backend
        analyzeText(text).then((result) => {
            console.log("Backend returned:", result);
            // STORE RESULT FOR POPUP.JS
            chrome.storage.local.set({
                text: text,
                label: result.label,
                score: result.score,
                categories: result.categories
            });
            console.log("Stored result successfully");
        });
    }
});

// CALL PYTHON BACKEND API
async function analyzeText(text) {
    console.log("Sending request to backend...");
    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });
        console.log("Response received");
        const data = await response.json();
        console.log("Parsed JSON:", data);
        return data;
    } catch (error) {
        console.error("BACKEND ERROR:", error);
        return {
            label: "error",
            score: 0,
            categories: {}
        };
    }
}