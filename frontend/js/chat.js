async function checkAuth() {
    const res = await fetch("/api/auth/status");
    const data = await res.json();

    if (!data.logged_in) {
        window.location.href = "index.html";
        return;
    }

    document.getElementById("userEmail").textContent =
        "Logged in as: " + data.user.email;
}

//To load all the chats in your chats list
async function loadAllChats() {
    const res = await fetch(`/api/chat/listallchats`);
    if (!res.ok) return;

    const data = await res.json();

    const chatsDict = data.chats || {};
    const chatValues = Object.values(chatsDict);

    const list = document.getElementById("allChats");
    list.innerHTML = "";

    if (chatValues.length === 0) {
        list.innerHTML = "<p>You are not in any chats.</p>";
        return;
    }

    chatValues.forEach(c => {
        const li = document.createElement("li");
        li.className = "chat-item";
        li.textContent = c.name;
        li.style.cursor = "pointer";

        li.addEventListener("click", () => openChatPopup(c));
        list.appendChild(li);
    });
}


const createBtn = document.getElementById("createChatBtn");
const chatNameInput = document.getElementById("newChat")

//for the chat popup
function openChatPopup(chat) {

    document.getElementById("chatPopupTitle").textContent = chat.name;
    document.getElementById("chatPopupID").textContent = chat.chat_id
    document.getElementById("chatPopupMembers").textContent = chat.members.join(", ");

    const messagesDiv = document.getElementById("chatMessages");
    messagesDiv.innerHTML = "";

    if (chat.messages && chat.messages.length > 0) {
        chat.messages.forEach(msg => {
            const p = document.createElement("p");
            p.textContent = msg;
            messagesDiv.appendChild(p);
        });
    } else {
        messagesDiv.innerHTML = "<p>No messages yet.</p>";
    }

    document.getElementById("sendChatMessageBtn").onclick = async () => {
        const messageInput = document.getElementById("chatMessageInput");
        const message = messageInput.value.trim();
        if (!message) return;

        const res = await fetch("/api/chat/send", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ chat_id: chat.chat_id, message })
        });

        const result = await res.json();
        if (!result.success) {
            alert(result.error);
            return;
        }

        messageInput.value = "";
        openChatPopup(result.study);
    };

    document.getElementById("closeChatPopupBtn").onclick = () => {
        document.getElementById("chatPopup").style.display = "none";
    };

    document.getElementById("chatPopup").style.display = "block";
}

document.getElementById("createChatBtn").addEventListener("click", async () => {
    const name = document.getElementById("newChat").value.trim();

    const res = await fetch("/api/chat/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadAllChats();
    }
});

document.getElementById("joinChatBtn").addEventListener("click", async () => {
    const id = document.getElementById("newChat").value.trim();

    if (!id) {
        err.textContent = "Chat ID required.";
        return;
    }

    const res = await fetch("/api/chat/join", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadAllChats();
    }
});

document.getElementById("leaveChatBtn").addEventListener("click", async () => {
    const id = document.getElementById("newChat").value.trim();

    if (!id) {
        err.textContent = "Chat ID required.";
        return;
    }

    const res = await fetch("/api/chat/leave", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadAllChats();
    }
});
checkAuth();
loadAllChats();