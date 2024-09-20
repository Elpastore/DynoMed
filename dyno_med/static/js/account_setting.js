function confirmAction(actionType) {
    if (actionType === 'deactivate') {
        return confirm(`Are you sure you want to ${actionType} your account?`);
    }
    return confirm(`Are you sure you want to change ${actionType}?`);
}

// Function to prepare POST data based on the action type
function preparePostData(actionType) {
    let postData = {};  // Variable name was incorrect before

    if (actionType === 'email') {
        postData = { email: document.getElementById('emailInput').value };
    } else if (actionType === 'username') {
        postData = { username: document.getElementById('usernameInput').value };
    } else if (actionType === 'password') {
        postData = {
            old_password: document.getElementById('oldPassword').value,  // Fixed issue here
            new_password: document.getElementById('newPassword').value,
            confirm_password: document.getElementById('confirmPassword').value
        };
    } else if (actionType === 'deactivate') {
        postData = { deactivate: true };
    }

    return postData;
}

// Function to send POST request and handle response
function sendPostRequest(postData, actionType) {
    fetch('/user_page/account_setting', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Fixed case here
            //'X-CSRFToken': '{{ csrf_token() }}'  // Uncomment if CSRF token is enabled
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())  // Fixed typo in 'response'
    .then(data => {
        if (data.success) {
            alert(data.message);
            if (actionType === 'deactivate') {
                window.location.href = '/';
            }
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error);
    });
}

// Function to handle button click event
function handleButtonClick(button) {
    const actionType = button.getAttribute('data-type');
    const confirmed = confirmAction(actionType);

    if (confirmed) {
        const postData = preparePostData(actionType);  // Fixed typo here
        sendPostRequest(postData, actionType);
    }
}

// Add event listener to all changeSettingBtn buttons
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.changeSettingBtn').forEach(button => {
        button.addEventListener('click', function () {
            console.log('Button clicked:', this);  // Debugging line
            handleButtonClick(this);
        });
    });
});
