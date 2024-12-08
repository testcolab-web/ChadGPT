document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const modelSelect = document.getElementById("model-select");
    const loadingBall = document.getElementById("loading-ball");
    const themeToggle = document.getElementById("theme-toggle");
    const liveUpdates = document.getElementById("live-updates");
    const welcomeMessage = document.getElementById("welcome-message");

    let darkMode = true;

    // Theme toggle
    themeToggle.addEventListener("click", () => {
        darkMode = !darkMode;
        document.body.style.backgroundColor = darkMode ? "#121212" : "#ffffff";
        document.body.style.color = darkMode ? "#ffffff" : "#000000";
    });

    // Remove welcome message on first input
    userInput.addEventListener("input", () => {
        if (welcomeMessage) {
            welcomeMessage.style.display = "none";
        }
    });

    // Send button click handler
    sendButton.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (!message || message.length > 500) {
            alert("Please enter a valid message (maximum 500 characters).");
            return;
        }

        // Add user message to chat log
        addMessageToChat("user", message);
        userInput.value = "";

        // Show loading ball and live updates
        loadingBall.style.display = "block";
        showLiveUpdates("⚫ Processing your request...");

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
                addMessageToChat("bot", `${botMessage} ${sourceUrl}`, true);
            }
        } catch (error) {
            addMessageToChat("bot", "Error: Unable to connect to the server.");
        } finally {
            // Hide loading ball and update live status
            loadingBall.style.display = "none";
            showLiveUpdates("⚫ Complete");
        }
    });

    // Function to show live updates
    function showLiveUpdates(stage) {
        liveUpdates.textContent = stage;
    }

    // Function to add messages to the chat log
    function addMessageToChat(sender, message, isAnimated = false) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${sender}-message`;

        if (isAnimated) {
            // Add typewriter effect for bot messages
            let i = 0;
            const interval = setInterval(() => {
                messageElement.innerHTML += message.charAt(i);
                i++;
                if (i >= message.length) clearInterval(interval);
            }, 50);
        } else {
            messageElement.innerHTML = message;
        }

        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
