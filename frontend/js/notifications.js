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
async function fetchNotifications(){
    try {
        const response = await fetch('/api/notifications');
        const data = await response.json();

        if(!data.success) return;
        renderNotifications(data.notifications);


    }
    catch(err){
        console.error(err);
    }
}


function renderNotifications(notifications){
    const list = document.getElementById('notificationslist')
    list.innerHTML = '';

    if(notifications.length === 0){
        list.innerHTML = '<li>No notifications.</li>'
        return;
    }
    notifications.forEach(notification => {
        const li = document.createElement('li');
        li.style.marginBottom = '10px';
        li.className = "group-item";

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = notification.read;
        checkbox.addEventListener('change', () => markAsRead(notification.id, checkbox.checked, li));

        const span = document.createElement('span');
        span.textContent = notification.message;
        span.style.margin = '0 10px';
        if(notification.read) span.style.textDecoration = 'line-through';

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.addEventListener('click', () => deleteNotification(notification.id, li));

        li.append(span);
        li.append(checkbox);
        li.append(deleteBtn);
        list.appendChild(li);

    });

}

async function markAsRead(notificationID, isRead, liElement){
    try{
        const res = await fetch('/api/notifications/read', {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({id: notificationID})
        });

        const data = await res.json();
        if(!data.success) return;
        liElement.querySelector('span').style.textDecoration = isRead ? 'line-through': 'none';
    }
    catch(err){
        console.error(err);
    }
}

async function deleteNotification(notificationID, liElement){
    try {
        const res = await fetch('/api/notifications/delete', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: notificationID})
        });

        const data = await res.json();
        if(!data.success) return;
        liElement.remove();

    }
    catch(err){
        console.error(err);
    }
}
checkAuth();
fetchNotifications();