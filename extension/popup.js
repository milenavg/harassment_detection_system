chrome.storage.local.set({
    text: "example message",
    label: "toxic",
    score: 0.92,
    categories: { harassment: true }
});
document.addEventListener("DOMContentLoaded", () => {

    // GET UI ELEMENTS
    const resultEl = document.getElementById("result");
    const scoreEl = document.getElementById("score");
    const lastTextEl = document.getElementById("lastText");

    // LOAD DATA FROM EXTENSION STORAGE
    // (data is written by background.js later)
    chrome.storage.local.get(
        ["text", "label", "score", "categories"],
        (data) => {

            // LAST ANALYZED TEXT
            if (data.text) {
                lastTextEl.textContent = data.text;
            }

            // RESULT (SAFE / TOXIC)
            if (data.label) {
                resultEl.textContent = data.label.toUpperCase();

                if (data.label === "toxic") {
                    resultEl.classList.add("toxic");
                } else {
                    resultEl.classList.add("safe");
                }
            }

            // SEVERITY SCORE
            if (data.score !== undefined) {
                scoreEl.textContent = data.score;
            }

            // CATEGORIES (future UI)
            if (data.categories) {
                console.log("Categories:", data.categories);
            }
        }
    );
});