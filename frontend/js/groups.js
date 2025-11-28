async function loadAllGroups() {
    const res = await fetch("/api/group/listall")
    if(!res.ok) return;

    const data = await res.json();

    const list = document.getElementById("allGroups");
    list.innerHTML = "";

    if(data.groups.length === 0 ){
        list.innerHTML = "<p>There are no groups.</p>";
        return
    }

    data.groups.forEach( g => {
        const li = document.createElement("li");
        li.className = "group-item";
        li.textContent = `ID: ${g.id} — ${g.name}`;
        list.appendChild(li);
    })

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


loadAllGroups();
