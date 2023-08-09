/ JavaScript code to handle form submission and redirection after login

const loginForm = document.querySelector('form');

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Get user input from the form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Perform login validation (check email and password against stored data or API)

    // If login is successful, redirect the user to the dashboard.html page
    window.location.href = 'dashboard.html';

    // If login fails, show an error message to the user
});

