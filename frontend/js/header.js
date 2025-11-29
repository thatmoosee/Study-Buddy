// header.js - Reusable header component
document.addEventListener('DOMContentLoaded', function() {
    const headerHTML = `
    <header>
        <nav>
            <ul>
                <li class="logo">
                    <img src="img/icon.png" alt="Study Buddy Logo" style="height: 35px;"/>
                </li>
                <li><a href="index.html">Home</a></li>
                <li><a href="groups.html">Groups</a></li>
                <li><a href="search.html">Search</a></li>
                <li><a href="chats.html">Chats</a></li>
                <li><a href="add_notifications.html">Notifications</a></li>
                <li><a href="logout.html">Logout</a></li>
            </ul>
        </nav>
    </header>
`;

    
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        headerPlaceholder.innerHTML = headerHTML;
    }
})