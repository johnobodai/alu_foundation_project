document.addEventListener("DOMContentLoaded", () => {
    // Get all the "Enroll Now" buttons
    const enrollButtons = document.querySelectorAll(".enroll-button");

    // Add click event listener to each button
    enrollButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Check if the user is logged in (you should have a function to do this)
            const isLoggedIn = checkUserLoginStatus(); // Replace with your authentication check function

            // If the user is not logged in, redirect to login/signup page
            if (!isLoggedIn) {
                window.location.href = "login.html"; // Replace with your login/signup page URL
            } else {
                // If the user is logged in, proceed with enrollment
                // Implement the enrollment logic here (e.g., display enrollment form/modal, handle payment, etc.)
                // For this example, we'll simply show an alert message
                alert("You have successfully enrolled in the course!");
            }
        });
    });
});

