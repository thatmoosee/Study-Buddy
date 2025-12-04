async function checkAuth() {
    const res = await fetch("/api/auth/status");
    const data = await res.json();

    if (!data.logged_in) {
        window.location.href = "index.html";
        return;
    }
    const id = data.user.user_id;
    const email = data.user.email;
    document.body.setAttribute('user_id', id);
    document.body.setAttribute('user_email', email);
    document.getElementById("userEmail").textContent =
        "Logged in as: " + email;
}

async function loadFilteredGroups(filterType, filterValue){
    const res = await fetch("/api/group/filter", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            type: filterType,
            value: filterValue
        })
    });

    if(!res.ok) return;

    const data = await res.json();
    const groups = data.groups;
    const list = document.getElementById("allGroups");
    list.innerHTML = "";

    if(groups.length === 0){
        list.innerHTML = "<p>No matching groups.</p>";
        return;
    }

    groups.forEach(g=> {
        const li = document.createElement("li");
        li.className = "group-item";
        li.textContent = `${g.name}`;

        li.style.cursor = "pointer";
        li.addEventListener("click", () => {
            openGroupInfo(g);
        });
        list.appendChild(li);
    })
}
async function loadSessions(){
    const res = await fetch("/api/study_schedule/get")
    if(!res.ok) return;

    const data = await res.json();

    const list = document.getElementById("reminderList")
    list.innerHTML = "";

    if(data.study.length === 0){
        list.innerHTML = "<p>There are no sessions.</p>";
        return;
    }

    data.study.forEach( session => {
        const li = document.createElement("li");
        li.className = "group-item";
        li.textContent = `${session.title} ${session.start_time} - ${session.end_time}`;
        list.appendChild(li)
    });
}

document.getElementById("scheduleSession").addEventListener("click", async () => {
    const popup = document.getElementById("studySessionPopup");
    const groupInfoPopup = document.getElementById("groupInfoPopup");
    groupInfoPopup.style.display = "none";
    popup.style.display = "flex";

});

const closeScheduleBtn = document.getElementById('closeScheduleBtn');
const createScheduleBtn = document.getElementById('createScheduleBtn');

closeScheduleBtn.addEventListener("click", () => {
    document.getElementById("studySessionPopup").style.display = "none";
});

createScheduleBtn.addEventListener("click", async () => {

    const session_name = document.getElementById("session_name").value;
    const start_date = document.getElementById("start_time").value;
    const end_date = document.getElementById("end_time").value;
    const popup = document.getElementById("groupInfoPopup");
    const id = popup.getAttribute('group_id').trim();
    const res = await fetch("/api/study_schedule/create", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            session_name: session_name,
            start_date: start_date,
            end_date: end_date,
            group_id: id
        })
    });
    const data = await res.json();
    popup.style.display = "none";
    loadSessions();
});

document.getElementById("joinGroupBtn").addEventListener("click", async () => {
    const popup = document.getElementById("groupInfoPopup");
    const err = document.getElementById("joinGroupError");
    err.textContent = "";
    const id = popup.getAttribute('group_id').trim();
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
        loadAllGroups();
    }
});

document.getElementById("leaveGroupBtn").addEventListener("click", async () => {
    const popup = document.getElementById("groupInfoPopup");
    const err = document.getElementById("leaveGroupError");
    err.textContent = "";
    const id = popup.getAttribute("group_id");
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
        loadAllGroups();
        document.getElementById("groupInfoPopup").style.display = "none";
    }
});
async function loadAllGroups() {
    const res = await fetch("/api/group/listall")
    if(!res.ok) return;

    const data = await res.json();

    const list = document.getElementById("allGroups");
    list.innerHTML = "";

    if(data.groups.length === 0 ){
        list.innerHTML = "<p>There are no groups.</p>";
        return;
    }

    data.groups.forEach( g => {
        const li = document.createElement("li");
        li.className = "group-item";
        li.textContent = `${g.name}`;

        li.style.cursor = "pointer";
        li.addEventListener("click", () => {
            openGroupInfo(g);
        });
        list.appendChild(li);
    })

}

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


const popup = document.getElementById("filterPopup");
const input = document.getElementById("filterInput");

document.getElementById("FilterGroup").addEventListener("click", () => {
    popup.style.display = "flex";
    input.value = "";
    input.focus();
});

document.getElementById("filterCancelBtn").addEventListener("click", () => {
    popup.style.display = "none";
});

document.getElementById("filterConfirmBtn").addEventListener("click", () => {
    const filterValue = input.value.trim();
    if (!filterValue) return;

    const filterType = document.querySelector('input[name="filterType"]:checked').value;

    popup.style.display = "none";
    loadFilteredGroups(filterType, filterValue);
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

    const joinButton = document.getElementById('joinGroupBtn');
    const leaveButton = document.getElementById('leaveGroupBtn');
    const scheduleSessionButton = document.getElementById('scheduleSession');
    const user_email = document.body.getAttribute('user_email');
    const isMember = group.members.includes(user_email);
    if(isMember){
        scheduleSessionButton.style.display="flex";
        joinButton.style.display = "none";
        leaveButton.style.display = 'block';
    }
    else{
        scheduleSessionButton.style.display = "none";
        joinButton.style.display = "block";
        leaveButton.style.display = "none";

    }
    popup.style.display = "flex";
}

document.getElementById("groupInfoCloseBtn").addEventListener("click", () => {
    document.getElementById("groupInfoPopup").style.display = "none";
});

const createBtn = document.getElementById("createGroupBtn");
const groupNameInput = document.getElementById("newGroupName");

const createPopup = document.getElementById("createGroupPopup");
const groupDisplay = document.getElementById("newGroupDisplay");
const groupClassInput = document.getElementById("newGroupClass");
const groupTimesInput = document.getElementById("newGroupTimes");
const createConfirmBtn = document.getElementById("createGroupConfirmBtn");
const createCancelBtn = document.getElementById("createGroupCancelBtn");

createBtn.addEventListener("click", () => {
    groupDisplay.textContent = "";
    groupClassInput.value = "";
    groupTimesInput.value = "";
    createPopup.style.display = "flex";
});

createCancelBtn.addEventListener("click", () => {
    createPopup.style.display = "none";
});

createConfirmBtn.addEventListener("click", async () => {
    const groupName = groupNameInput.value.trim();
    const className = groupClassInput.value.trim();
    const times = groupTimesInput.value.trim();

    if (!className || !groupName) {
        alert("Please enter a class and group name.");
        return;
    }
    const res = await fetch("/api/group/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: groupName,
            specified_class: className,
            study_times: times.split(",").map(t => t.trim())
        })
    });
    if (!res.ok) {
        alert(data.error || "Failed to create group.");
        return;
    }

    createPopup.style.display = "none";
    groupNameInput.value = "";
    loadGroups();
    loadAllGroups();
});
checkAuth();
loadGroups();
loadSessions();
loadAllGroups();