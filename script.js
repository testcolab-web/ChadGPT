document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const modelSelect = document.getElementById("model-select");
    const loadingBall = document.getElementById("loading-ball");
    const themeToggle = document.getElementById("theme-toggle");

    let darkMode = true;

    // Theme toggle
    themeToggle.addEventListener("click", () => {
        darkMode = !darkMode;
        document.body.style.backgroundColor = darkMode ? "#121212" : "#ffffff";
        document.body.style.color = darkMode ? "#ffffff" : "#000000";
    });

    // Send button click handler
    sendButton.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat log
        addMessageToChat("user", message);
        userInput.value = "";

        // Show loading ball
        loadingBall.style.display = "block";

        const selectedModel = modelSelect.value;

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, model: selectedModel }),
            });

            const data = await response.json();
            if (data.error) {
                addMessageToChat("bot", `Error: ${data.error}`);
            } else {
                const botMessage = data.reply;
                const sourceUrl = data.source_url ? `<a href="${data.source_url}" target="_blank">Source</a>` : "";
                addMessageToChat("bot", `${botMessage} ${sourceUrl}`);
            }
        } catch (error) {
            addMessageToChat("bot", "Error: Unable to connect to the server.");
        } finally {
            // Hide loading ball
            loadingBall.style.display = "none";
        }
    });

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${sender}-message`;
        messageElement.innerHTML = message;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
