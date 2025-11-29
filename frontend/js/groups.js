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

function openGroupInfo(group) {
    const popup = document.getElementById("groupInfoPopup");
    document.getElementById("groupTitle").textContent = group.name;
    document.getElementById("groupId").textContent = group.id;
    document.getElementById("groupMembers").textContent = group.members.join(", ");
    if(group.specified_class.length == 0){
        document.getElementById("specifiedClass").textContent = "None";
    }
    else{
        document.getElementById("specifiedClass").textContent = group.specified_class;

    }
    if(group.study_times.length == 0){
        document.getElementById("studyTimes").textContent = "None";
    }
    else{
        document.getElementById("studyTimes").textContent = group.study_times.join(",");
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
    const groupName = groupNameInput.value.trim();
    if (!groupName) {
        document.getElementById("createGroupError").textContent = "Please enter a group name.";
        return;
    }
    document.getElementById("createGroupError").textContent = "";

    groupDisplay.textContent = groupName;
    groupClassInput.value = "";
    groupTimesInput.value = "";
    createPopup.style.display = "flex";
});

createCancelBtn.addEventListener("click", () => {
    createPopup.style.display = "none";
});

createConfirmBtn.addEventListener("click", async () => {
    const className = groupClassInput.value.trim();
    const times = groupTimesInput.value.trim();

    if (!className || !times) {
        alert("Please enter both class and study times.");
        return;
    }
    const res = await fetch("/api/group/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: groupDisplay.textContent,
            specified_class: className,
            study_times: times.split(",").map(t => t.trim())
        })
    });

    if (!res.ok) {
        alert("Failed to create group.");
        return;
    }

    createPopup.style.display = "none";
    groupNameInput.value = "";
    loadGroups();
    loadAllGroups();
});
loadGroups();
loadAllGroups();