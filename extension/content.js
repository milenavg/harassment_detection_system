// 1. CAPTURE SELECTED TEXT (manual highlight)
document.addEventListener("mouseup", () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 3) {
        sendToBackground(selectedText);
    }
});

// 2. CAPTURE TYPED TEXT (input + textarea)
document.addEventListener("input", (event) => {
    const target = event.target;
    // Only process text inputs
    if (
        target.tagName === "TEXTAREA" ||
        (target.tagName === "INPUT" && target.type === "text")
    ) {
        const text = target.value;
        if (text && text.length > 3) {
            sendToBackground(text);
        }
    }
});

// 3. SEND MESSAGE TO BACKGROUND SCRIPT
function sendToBackground(text) {
    chrome.runtime.sendMessage({
        type: "ANALYZE_TEXT",
        text: text
    });
    console.log("Sent for analysis:", text);
}

// 4. OPTIONAL: CHAT DETECTION (MutationObserver)
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1) {
                const text = node.innerText;
                if (text && text.length > 20 && text.length < 500) {
                    sendToBackground(text);
                }
            }
        });
    });
});


// Start observing page changes
observer.observe(document.body, {
    childList: true,
    subtree: true
});