document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("chatbot-fab")) return;

    const SESSION_TIMEOUT = 10 * 60 * 1000; // 10 minutes
    const STORAGE_KEY = "kindatech_chat_session";

    let sessionTimer = null;
    let attachments = [];

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

        <div id="chatbot-messages"></div>

        <div id="chatbot-attachments-summary" style="padding:5px; font-size:0.85em; color:#555;"></div>

        <div id="chatbot-input">
            <button id="chatbot-attachment">📎</button>
            <input id="chatbot-text" type="text" placeholder="Ask me anything…" />
            <input type="file" id="chatbot-file" style="display:none" multiple />
            <button id="chatbot-send">➤</button>
        </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(chatWindow);

    const messages = document.getElementById("chatbot-messages");
    const attachmentsSummary = document.getElementById("chatbot-attachments-summary");
    const input = document.getElementById("chatbot-text");
    const sendBtn = document.getElementById("chatbot-send");
    const attachmentBtn = document.getElementById("chatbot-attachment");
    const fileInput = document.getElementById("chatbot-file");

    /* ---------------- STORAGE ---------------- */

    function saveSession() {
        const sessionData = {
            messages: messages.innerHTML,
            timestamp: Date.now()
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(sessionData));
    }

    function loadSession() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) return false;

        const sessionData = JSON.parse(saved);
        const now = Date.now();

        if (now - sessionData.timestamp > SESSION_TIMEOUT) {
            localStorage.removeItem(STORAGE_KEY);
            return false;
        }

        messages.innerHTML = sessionData.messages;
        return true;
    }

    function clearSessionStorage() {
        localStorage.removeItem(STORAGE_KEY);
    }

    /* ---------------- TIMER ---------------- */

    function startSessionTimer() {
        clearTimeout(sessionTimer);
        sessionTimer = setTimeout(() => {
            endSession();
        }, SESSION_TIMEOUT);
    }

    function resetSessionTimer() {
        clearTimeout(sessionTimer);
        startSessionTimer();
        saveSession();
    }

    function endSession() {
        messages.innerHTML = `
            <div class="msg bot">
                ⏳ Session expired due to inactivity (10 minutes).<br/><br/>
                Hi 👋 I’m your Kindatech AI assistant. How can I help you today?
            </div>
        `;

        attachments = [];
        updateAttachmentsSummary();
        input.value = "";
        fileInput.value = "";

        chatWindow.classList.remove("open");

        clearSessionStorage();
        clearTimeout(sessionTimer);
    }

    /* ---------------- INIT ---------------- */

    const restored = loadSession();

    if (!restored) {
        messages.innerHTML = `
            <div class="msg bot">
                Hi 👋 I’m your Kindatech AI assistant. I can help you with anything related to Kindatech.<br/>
                How can I help you today?
            </div>
        `;
        saveSession();
    }

    startSessionTimer();

    /* ---------------- EVENTS ---------------- */

    fab.onclick = () => {
        chatWindow.classList.toggle("open");
        input.focus();
        resetSessionTimer();
    };

    document.getElementById("chatbot-close").onclick = () => {
        chatWindow.classList.remove("open");
    };

    attachmentBtn.onclick = () => {
        fileInput.click();
        resetSessionTimer();
    };

    fileInput.addEventListener("change", () => {
        for (let i = 0; i < fileInput.files.length; i++) {
            attachments.push(fileInput.files[i]);
        }
        updateAttachmentsSummary();
        resetSessionTimer();
    });

    input.addEventListener("keypress", e => {
        resetSessionTimer();
        if (e.key === "Enter") sendMessage();
    });

    sendBtn.onclick = sendMessage;

    /* ---------------- ATTACHMENTS ---------------- */

    function updateAttachmentsSummary() {
        if (attachments.length === 0) {
            attachmentsSummary.textContent = "";
            return;
        }

        const names = attachments.map(f =>
            f.name.length > 20 ? f.name.slice(0, 17) + "..." : f.name
        );

        attachmentsSummary.textContent =
            `Attachments (${attachments.length}): ${names.join(", ")}`;
    }

    /* ---------------- MESSAGE LOGIC ---------------- */

    async function sendMessage() {
        const text = input.value.trim();
        if (!text && attachments.length === 0) return;

        resetSessionTimer();

        if (text) addMessage(text, "user");

        attachments.forEach(file =>
            addMessage(`📎 ${file.name}`, "user")
        );

        const filesToSend = [...attachments];
        attachments = [];
        updateAttachmentsSummary();
        input.value = "";
        fileInput.value = "";

        setLoading(true);

        try {
            let chatbotReply;

            if (filesToSend.length > 0) {
                chatbotReply = await sendFilesWithText(filesToSend, text);
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
        const response = await fetch(
            "/api/method/chatbot.api.chatbot_api.receive_user_input",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Frappe-CSRF-Token": frappe.csrf_token
                },
                body: JSON.stringify({ message })
            }
        );

        if (!response.ok) throw new Error("Request failed");
        const data = await response.json();
        return data.message || "No response from AI";
    }

    async function sendFilesWithText(files, text) {
        const formData = new FormData();
        files.forEach(file => formData.append("files", file));
        formData.append("text", text);

        const response = await fetch(
            "/api/method/chatbot.api.chatbot_api.upload_file_with_text",
            {
                method: "POST",
                headers: {
                    "X-Frappe-CSRF-Token": frappe.csrf_token
                },
                body: formData
            }
        );

        if (!response.ok) throw new Error("Request failed");
        const data = await response.json();
        return data.message || "Files processed successfully!";
    }

    function addMessage(text, type = "bot") {
        const msg = document.createElement("div");
        msg.className = `msg ${type}`;
        msg.innerHTML = text;
        messages.appendChild(msg);
        msg.scrollIntoView({ behavior: "smooth" });
        saveSession();
    }

    function setLoading(loading) {
        sendBtn.disabled = loading;
        attachmentBtn.disabled = loading;
    }
});
