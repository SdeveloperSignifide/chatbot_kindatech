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
                Hi 👋 I’m your Kindatech AI assistant. I can help you with anything related to Kindatech.<br/>
                How can I help you today?
            </div>
        </div>

        <div id="chatbot-input">
            <button id="chatbot-attachment">📎</button>
            <input id="chatbot-text" type="text" placeholder="Ask me anything…" />
            <input type="file" id="chatbot-file" style="display:none" />
            <button id="chatbot-send">➤</button>
        </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(chatWindow);

    const messages = document.getElementById("chatbot-messages");
    const input = document.getElementById("chatbot-text");
    const sendBtn = document.getElementById("chatbot-send");
    const attachmentBtn = document.getElementById("chatbot-attachment");
    const fileInput = document.getElementById("chatbot-file");

    fab.onclick = () => {
        chatWindow.classList.toggle("open");
        input.focus();
    };

    document.getElementById("chatbot-close").onclick = () => {
        chatWindow.classList.remove("open");
    };

    attachmentBtn.onclick = () => fileInput.click();

    input.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    sendBtn.onclick = sendMessage;

    async function sendMessage() {
        const text = input.value.trim();
        const file = fileInput.files[0];

        if (!text && !file) return;

        if (text) addMessage(text, "user");
        if (file) addMessage(`📎 ${file.name}`, "user");

        input.value = "";
        fileInput.value = "";
        setLoading(true);

        try {
            let chatbotReply;
            if (file) {
                chatbotReply = await sendFileWithText(file, text);
            } else {
                chatbotReply = await sendUserInput(text);
            }
            addMessage(chatbotReply, "bot");
        } catch (err) {
            console.error(err);
            addMessage("Something went wrong!", "bot");
        } finally {
            setLoading(false);
        }
    }

    async function sendUserInput(message) {
        const response = await fetch("/api/method/chatbot.api.chatbot_api.receive_user_input", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Frappe-CSRF-Token": frappe.csrf_token
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error("The request failed");
        const data = await response.json();
        return data.message || "No response from AI";
    }

    async function sendFileWithText(file, text) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("text", text);  // include the text input

        const response = await fetch("/api/method/chatbot.api.chatbot_api.upload_file_with_text", {
            method: "POST",
            headers: {
                "X-Frappe-CSRF-Token": frappe.csrf_token
            },
            body: formData
        });

        if (!response.ok) throw new Error("Request failed");
        const data = await response.json();
        return data.message || "File processed successfully!";
    }

    function addMessage(text, type = "bot") {
        const msg = document.createElement("div");
        msg.className = `msg ${type}`;
        msg.innerHTML = typeof text === "object" ? JSON.stringify(text, null, 2) : text;
        messages.appendChild(msg);
        msg.scrollIntoView({ behavior: "smooth" });
    }

    function setLoading(loading) {
        sendBtn.disabled = loading;
        attachmentBtn.disabled = loading;
    }
});
