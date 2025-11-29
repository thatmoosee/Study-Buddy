
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

async function loadFriends() {
    const res = await fetch("/api/friends/list");
    if (!res.ok) return;

    const data = await res.json();
    const list = document.getElementById("friendList");
    list.innerHTML = "";

    if (data.friends.length === 0 || !data.friends) {
        list.innerHTML = "<p>You have no friends yet.</p>";
        return;
    }

    data.groups.forEach(id => {
        const li = document.createElement("li");
        li.textContent =  id;
        list.appendChild(li);
    });
}

document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "index.html";
});

document.getElementById("editProfileBtn").addEventListener("click", () => {
    window.location.href = "editProfile.html";
});

/*
Join a group
*/
document.getElementById("addFriendBtn").addEventListener("click", async () => {
    const id = document.getElementById("newFriend").value.trim();

    if (!id) {
        err.textContent = "Friend ID required.";
        return;
    }

    const res = await fetch("/api/friends/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ friend_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadFriends();
    }
});

/*
Leave a group
*/
document.getElementById("removeFriendBtn").addEventListener("click", async () => {
    const id = document.getElementById("newFriend").value.trim();

    if (!id) {
        err.textContent = "Friend ID required.";
        return;
    }

    const res = await fetch("/api/friends/remove", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ friend_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadFriends();
    }
});

checkAuth();
loadFriends();
