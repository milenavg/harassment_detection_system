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

    if (
        target.tagName === "TEXTAREA" ||
        (target.tagName === "INPUT" && target.type === "text")
    ) {
        const text = target.value?.trim();

        if (text && text.length > 3) {
            throttledSend(text);
        }
    }
});


// 3. SIMPLE THROTTLE
let lastSentText = "";
let lastSentTime = 0;

function throttledSend(text) {
    const now = Date.now();

    if (text === lastSentText && now - lastSentTime < 1500) {
        return;
    }

    lastSentText = text;
    lastSentTime = now;

    sendToBackground(text);
}


// 4. SEND MESSAGE TO BACKEND
function sendToBackground(text) {
    chrome.runtime.sendMessage({
        type: "ANALYZE_TEXT",
        text: text
    });

    console.log("Sent for analysis:", text);
}


// 5. CHAT DETECTION 
const seenTexts = new Set();
let timeout;

const observer = new MutationObserver((mutations) => {

    for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {

            if (node.nodeType !== 1) continue;

            const text = node.innerText?.trim();

            if (!text || text.length < 20 || text.length > 500) continue;

            if (seenTexts.has(text)) continue;
            seenTexts.add(text);

            clearTimeout(timeout);

            timeout = setTimeout(() => {
                sendToBackground(text);
            }, 800);
        }
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});