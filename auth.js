// auth.js

// Function to set a user credential in local storage
function registerUser(username, password) {
    const user = { username, password };
    localStorage.setItem('user', JSON.stringify(user));
    alert('Registration successful! You can now log in.');
}

// Function to log in the user
function loginUser(username, password) {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.username === username && user.password === password) {
        alert('Login successful!');
        // Redirect to dashboard or another page
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid username or password.');
    }
}

// Function to check if user is already logged in
function checkLogin() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        // Redirect to dashboard if already logged in
        window.location.href = 'dashboard.html';
    }
}

// Function to log out the user
function logoutUser() {
    localStorage.removeItem('user');
    alert('You have been logged out.');
    // Redirect to login page
    window.location.href = 'login.html';
}
