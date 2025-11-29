async function checkAuth() {
    const res = await fetch("/api/auth/status");
    const data = await res.json();

    if (!data.logged_in) {
        window.location.href = "index.html"; // Redirect to login if not logged in
    }
}

document.getElementById("saveProfileBtn").addEventListener("click", async () => {
    const name = document.getElementById("name").value.trim();
    const major = document.getElementById("major").value.trim();
    const availability = document.getElementById("availability").value.trim();

    if (!name) {
        alert("Name is required");
        return;
    }

    const data = {
        name,
        major,
        availability
    };

    const res = await fetch(`/api/profile/upload`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await res.json();
    if (result.success) {
        alert("Profile updated successfully!");
        window.location.href = "profile.html";
    } else {
        alert("Error: " + result.error);
    }
});

document.getElementById("CancelBtn").addEventListener("click", () => {
    window.location.href = "profile.html";
});

checkAuth();