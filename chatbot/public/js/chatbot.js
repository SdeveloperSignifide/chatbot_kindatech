
$(document).ready(function () {
    // Avoid loading twice
    if (document.getElementById("chatbot-fab")) return;

    // Floating button
    const fab = document.createElement("div");
    fab.id = "chatbot-fab";
    fab.innerHTML = "💬";

    // Chat window
    const chatWindow = document.createElement("div");
    chatWindow.id = "chatbot-window";
    chatWindow.innerHTML = `
        <div id="chatbot-header">
            Chatbot
            <span id="chatbot-close" style="cursor:pointer">✖</span>
        </div>
        <div id="chatbot-messages"></div>
        <div id="chatbot-input">
            <input type="text" id="chatbot-text" placeholder="Type a message..." />
            <button id="chatbot-send">Send</button>
        </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(chatWindow);

    // Toggle chat window
    fab.addEventListener("click", () => {
        chatWindow.classList.toggle("open");
    });

    // Close button
    document
        .getElementById("chatbot-close")
        .addEventListener("click", () => {
            chatWindow.classList.remove("open");
        });

    // Send message
    document
        .getElementById("chatbot-send")
        .addEventListener("click", sendMessage);
});
