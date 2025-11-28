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

function openGroupInfo(group){
    alert(`Group Info:\nID: ${group.id}\nName: ${group.name}\nMembers: ${group.members.join(", ")}`);
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

    console.log("Filtering groups by:", filterValue);

    popup.style.display = "none";
});

function openGroupInfo(group) {
    const popup = document.getElementById("groupInfoPopup");
    document.getElementById("groupTitle").textContent = group.name;
    document.getElementById("groupId").textContent = group.id;
    document.getElementById("groupMembers").textContent = group.members.join(", ");

    popup.style.display = "flex";
}

document.getElementById("groupInfoCloseBtn").addEventListener("click", () => {
    document.getElementById("groupInfoPopup").style.display = "none";
});


loadAllGroups();
