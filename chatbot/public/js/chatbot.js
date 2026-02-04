document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("chatbot-fab")) return;


    const fab = document.createElement("div");
    fab.id = "chatbot-fab";
    fab.innerHTML = "🤖";

    const chatWindow = document.createElement("div");
    chatWindow.id = "chatbot-window";
    chatWindow.innerHTML = `
        <div id="chatbot-header">
            <div class="title">Kindatech Assistant</div>
            <span id="chatbot-close">✕</span>
        </div>

        <div id="chatbot-messages">
            <div class="msg bot">
                Hi 👋 I’m your Kindatech AI assistant.<br/>
                How can I help you today?
            </div>
        </div>

        <div id="chatbot-input">
         <button id="chatbot-attachment">📎</button>
            <input id="chatbot-text" type="text" placeholder="Ask me anything…" />
            <button id="chatbot-send">➤</button>
        </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(chatWindow);

    // Toggle open
    fab.onclick = () => {
        chatWindow.classList.toggle("open");
        document.getElementById("chatbot-text").focus();
    };

    document.getElementById("chatbot-close").onclick = () => {
        chatWindow.classList.remove("open");
    };

    document.getElementById("chatbot-send").onclick = sendMessage;

    document.getElementById("chatbot-text").addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const input = document.getElementById("chatbot-text");
        const messages = document.getElementById("chatbot-messages");

        if (!input.value.trim()) return;

        addMessage(input.value, "user");
        input.value = "";

        // Fake AI response (replace with backend call)


        
        setTimeout(() => {
            addMessage("🤖 I’m thinking… AI response will go here.");
        }, 600);
    }

    function addMessage(text, type) {
        const msg = document.createElement("div");
        msg.className = `msg ${type}`;
        msg.innerHTML = text;
        document.getElementById("chatbot-messages").appendChild(msg);
        msg.scrollIntoView({ behavior: "smooth" });
    }
});
