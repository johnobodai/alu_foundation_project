document.addEventListener("DOMContentLoaded", () => {
    // Get all the "Enroll Now" buttons
    const enrollButtons = document.querySelectorAll(".enroll-button");

// Get the form data
var username = document.getElementById("username").value;
var password = document.getElementById("password").value;
var email = document.getElementById("email").value;

function validateRegistrationForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var emailRegex = /^\S+@\S+\.\S+$/;

    if (!username) {
        document.getElementById("username-error").textContent = "Please eneter a username.";
        return false;
    } else {
        document.getElementById("username-error").textContent = "";
    }

    if(!password) {
        document.getElementById("password-error").textContent = "Please enter a password.";
        return false;
    } else {
        document.getElementById("password-error").textContent = "";
    }

    if(!email) {
        document.getElementById("email-error").textContent = "Please eneter an email address";
        return false;
    } else if (!emailRegex.test(email)) {
        document.getElementById("email-error").textContent = "Please enter a valid email address";
        return false;
    } else {
        document.getElementById("email-error").textContent = "";
    }

    return true;
}

console.log('Form data:', { username, password, email });

// Create an object with the form data
var formData = {
    username: username,
    password: password,
    email: email
};

// Send the form data to the server
fetch('/register', {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
})
.then(function(response) {
    // Check if the response has a successful status
    if (response.ok) {
        return response.json();
    } else {
        throw new Error('Registration failed'); // Throw an error if registration is unsuccessful
    }
})
.then(function(data) {
    //Handle the successfull registration response
    console.log(data.message);

    // Redirect to homepage
    window.location.href = ""
})
.catch(function(error) {
    console.error(error);
});

document.getElementById("login-form").addEventListener("submit", function(e) {
    e.preventDefault();

    // Get the form data
    var username = document.getElementById("login-username").value;
    var password = document.getElementById("login-password").value;
    
    console.log('Form data:', { username, password });
    
    //Create an object with the form data
    var formData = {
        username: username,
        password: password
    };

    //Send the form data to the server
    fetch('/login', {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(function(response) {
        // Check response status
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Login failed');
        }
    })
    .then(function(data) {
        console.log(data.message);

        window.location.href = "";
    })
    .catch(function(error) {
        console.error(error);

        alert('Login failed');
    });
});
    // Add click event listener to each button
    enrollButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Check if the user is logged in (you should have a function to do this)
            const isLoggedIn = checkUserLoginStatus(); // Replace with your authentication check function

            // Function to check if the user is logged in
            function checkUserLoginStatus() {
                return isLoggedIn;
            }

            // When the user logs in, set isLoggedIn to true
            function login() {
                isLoggedIn = true;
            }

            // When the user logs out, set isLoggedIn to false
            function logout() {
                isLoggedIn = false;
            }

            document.addEventListener("DOMContentLoaded", () => {
                // Get all the "Enroll Now" buttons
                const enrollButtons = document.querySelectorAll(".enroll-button");
            
                // Rest of the code...
                // (The fetch requests and other parts remain the same as in your previous code)
            
                // Add click event listener to each button
                enrollButtons.forEach(button => {
                    button.addEventListener("click", () => {
                        // Check if the user is logged in
                        const isLoggedIn = checkUserLoginStatus(); // Replace with your authentication check function
            
                        // The rest of the logic for enrollment based on login status
                        // (This part remains unchanged from your previous code)
                        // ...
                    });
                });
            });

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



