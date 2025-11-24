/******************************************
 * login is required if not — redirect to index.html
 ******************************************/
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

/******************************************
 * this pulls the users group the /api/group/list endpoint in app.py
 ******************************************/
async function loadGroups() {
    const res = await fetch("/api/group/list");
    if (!res.ok) return;

    const data = await res.json();
    const list = document.getElementById("groupList");
    list.innerHTML = "";

    if (data.groups.length === 0) {
        list.innerHTML = "<p>You are not in any groups.</p>";
        return;
    }

    data.groups.forEach(g => {
        const li = document.createElement("li");
        li.className = "group-item";
        li.textContent = `ID: ${g.id} — ${g.name}`;
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
 create group pulls it from app.py api/group/create
*/
document.getElementById("createGroupBtn").addEventListener("click", async () => {
    const name = document.getElementById("newGroupName").value.trim();
    const err = document.getElementById("createGroupError");

    err.textContent = "";
    if (!name) {
        err.textContent = "Group name required.";
        return;
    }

    const res = await fetch("/api/group/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, members: [] })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadGroups();
    }
});

/*
Join a group
*/
document.getElementById("joinGroupBtn").addEventListener("click", async () => {
    const id = document.getElementById("joinGroupId").value.trim();
    const err = document.getElementById("joinGroupError");
    err.textContent = "";

    if (!id) {
        err.textContent = "Group ID required.";
        return;
    }

    const res = await fetch("/api/group/join", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ group_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadGroups();
    }
});

/*
Leave a group
*/
document.getElementById("leaveGroupBtn").addEventListener("click", async () => {
    const id = document.getElementById("leaveGroupId").value.trim();
    const err = document.getElementById("leaveGroupError");
    err.textContent = "";

    if (!id) {
        err.textContent = "Group ID required.";
        return;
    }

    const res = await fetch("/api/group/leave", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ group_id: id })
    });

    const data = await res.json();
    if (!data.success) {
        err.textContent = data.error;
    } else {
        loadGroups();
    }
});

checkAuth();
loadGroups();
