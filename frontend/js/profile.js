/*
 * login is required if not — redirect to index.html
 */
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

/*
 * this pulls the users group the /api/group/list endpoint in app.py
*/

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
        li.textContent = `${g.name}`;

        li.style.cursor = "pointer";
        li.addEventListener("click", () => {
            openGroupInfo(g);
        });

        list.appendChild(li);
    });
}

document.getElementById('groupInfoCloseBtn').addEventListener('click', () => {
    document.getElementById('groupInfoPopup').style.display = "none";
});

async function openGroupInfo(group) {
    const popup = document.getElementById("groupInfoPopup");
    document.getElementById("groupTitle").textContent = group.name;
    document.getElementById("groupId").textContent = group.id;
    document.getElementById("groupMembers").textContent = group.members.join(", ");
    popup.setAttribute("group_id", group.id);
    if(group.specified_class.length === 0){

        document.getElementById("specifiedClass").textContent = "None";
    }
    else{
        document.getElementById("specifiedClass").textContent = group.specified_class;

    }
    if(group.study_times.length === 0){
        document.getElementById("studyTimes").textContent = "None";
    }
    else{
        document.getElementById("studyTimes").textContent = group.study_times.join(",");
    }

    popup.style.display = "flex";
}

document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "index.html";
});

document.getElementById("editProfileBtn").addEventListener("click", () => {
    window.location.href = "editProfile.html";
});

checkAuth();
loadGroups();
