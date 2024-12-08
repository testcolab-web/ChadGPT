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
        document.body.classList.toggle("dark-theme", darkMode);
    });

    // Send button click handler
    sendButton.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage("user", message);
        userInput.value = "";

        const selectedModel = modelSelect.value;
        setProcessIndicator("Processing...");

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, model: selectedModel }),
            });

            const data = await response.json();

            clearProcessIndicator();

            if (data.error) {
                addMessage("bot", `Error: ${data.error}`);
            } else {
                addMessage("bot", data.reply, true);
            }
        } catch (error) {
            clearProcessIndicator();
            addMessage("bot", "Network error. Please try again.");
        }
    });

    // Add message to chat log
    function addMessage(sender, message, isTypewriter = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;
        chatLog.appendChild(messageDiv);

        if (isTypewriter) {
            let i = 0;
            const typewriter = setInterval(() => {
                messageDiv.textContent += message.charAt(i);
                i++;
                if (i >= message.length) clearInterval(typewriter);
            }, 50);
        } else {
            messageDiv.textContent = message;
        }

        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Set process indicator
    function setProcessIndicator(text) {
        loadingBall.style.display = "block";
        loadingBall.textContent = text;
    }

    // Clear process indicator
    function clearProcessIndicator() {
        loadingBall.style.display = "none";
    }
});
