console.log("BACKGROUND SERVICE WORKER STARTED");

let lastText = "";
let lastTime = 0;

// LISTEN FOR MESSAGES FROM CONTENT.JS
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.type === "ANALYZE_TEXT") {

        const text = message.text;
        const now = Date.now();

        // PREVENT SPAM
        if (text === lastText && now - lastTime < 1500) {
            sendResponse({ status: "ignored" });
            return true;
        }

        lastText = text;
        lastTime = now;

        console.log("Received from content.js:", text);

        // async flow
        analyzeText(text)
            .then((result) => {

                console.log("Backend returned:", result);

                const safeResult = {
                    label: result.label || "unknown",
                    score: result.score || 0,
                    categories: result.categories || {}
                };

                // STORE RESULT
                chrome.storage.local.set({
                    text: text,
                    label: safeResult.label,
                    score: safeResult.score,
                    categories: safeResult.categories
                });

                // NOTIFY POPUP LIVE UPDATE
                chrome.runtime.sendMessage({
                    type: "NEW_RESULT",
                    data: safeResult
                });

                sendResponse({ status: "ok", result: safeResult });
            })
            .catch((error) => {

                console.error("ANALYSIS ERROR:", error);

                const fallback = {
                    label: "error",
                    score: 0,
                    categories: {}
                };

                sendResponse({ status: "error", result: fallback });
            });

        // IMPORTANT for async sendResponse
        return true;
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
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Parsed JSON:", data);
        return data;

    } catch (error) {
        console.error("BACKEND ERROR:", error);
        throw error;
    }
}