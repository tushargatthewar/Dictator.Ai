let isFirstMessage = true;
let chatHistory = [];

document.getElementById("sendBtn").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Toggle sidebar for mobile
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
}

// Close sidebar when clicking on history item (mobile)
function closeSidebarOnMobile() {
    if (window.innerWidth <= 768) {
        const sidebar = document.getElementById("sidebar");
        const overlay = document.getElementById("sidebarOverlay");
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    }
}

function newChat() {
    isFirstMessage = true;
    document.getElementById("messages").innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <h2>How can I help you today?</h2>
            <p>Start a conversation by typing a message below</p>
        </div>
    `;
    closeSidebarOnMobile();
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    // Remove empty state on first message
    if (isFirstMessage) {
        document.getElementById("messages").innerHTML = '';
        isFirstMessage = false;
    }

    displayMessage("You", message, "user-message");
    input.value = "";

    // Disable send button
    const sendBtn = document.getElementById("sendBtn");
    sendBtn.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        displayMessage("AI", data.reply, "bot-message");
        
        // Add to history
        addToHistory(message, data.reply);
    } catch (error) {
        removeTypingIndicator();
        displayMessage("AI", "Sorry, something went wrong. Please try again.", "bot-message");
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function displayMessage(sender, text, cssClass) {
    const messagesDiv = document.getElementById("messages");
    const isUser = cssClass === "user-message";
    
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${cssClass}`;
    messageDiv.innerHTML = `
        <div class="message-avatar">${isUser ? 'U' : 'AI'}</div>
        <div class="message-content">
            <div class="message-text">${text}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.parentElement.scrollTop = messagesDiv.parentElement.scrollHeight;
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById("messages");
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message typing-indicator-wrapper";
    typingDiv.id = "typingIndicator";
    typingDiv.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.parentElement.scrollTop = messagesDiv.parentElement.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
        indicator.remove();
    }
}

function addToHistory(userMsg, botMsg) {
    chatHistory.unshift({ user: userMsg, bot: botMsg });
    updateHistoryUI();
}

function updateHistoryUI() {
    const historyDiv = document.getElementById("chatHistory");
    historyDiv.innerHTML = chatHistory.slice(0, 10).map((chat, index) => `
        <div class="history-item" onclick="loadChat(${index})">
            <div class="history-title">${chat.user}</div>
            <div class="history-preview">${chat.bot.substring(0, 50)}...</div>
        </div>
    `).join('');
}

function loadChat(index) {
    const chat = chatHistory[index];
    isFirstMessage = false;
    document.getElementById("messages").innerHTML = '';
    displayMessage("You", chat.user, "user-message");
    displayMessage("AI", chat.bot, "bot-message");
    closeSidebarOnMobile();
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById("userInput").focus();
});