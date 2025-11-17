// header.js - Reusable header component
document.addEventListener('DOMContentLoaded', function() {
    const headerHTML = `
    <header>
        <div>
            <h1>Study Buddy</h1>
        </div>
        <nav>   <!-- FIXED -->
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="search.html">Search</a></li>
                <li><a href="filter_by_class.html">Filter by Class</a></li>
                <li><a href="filter_free_time.html">Filter by Free Time</a></li>
                <li><a href="chats.html">Chats</a></li>
                <li><a href="add_notifications.html">Notifications</a></li>
            </ul>
        </nav>
    </header>
`;

    
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        headerPlaceholder.innerHTML = headerHTML;
    }
})