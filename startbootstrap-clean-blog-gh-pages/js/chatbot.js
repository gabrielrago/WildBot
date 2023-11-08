$(document).ready(function () {
    console.log("Chatbot script loaded and ready.");
    const chatbotIcon = $('#chatbot-icon');
    const chatpane = $('#chatpane');
    const chatMessages = $('#chat-messages');
    const chatpaneHeader = $('#chatpane-header');
    const userInput = $('#user-input');
    const sendButton = $('#send-button');
    const clearChatButton = $('#clear-chat-button');
    let welcomeMessageShown = localStorage.getItem('welcomeMessageShown') === 'true';

    // Function to scroll to the bottom of the chat messages
    function scrollToBottom() {
        chatMessages.scrollTop(chatMessages.prop('scrollHeight'));
    }
    
    // Function to display the welcome message once
    function displayWelcomeMessage() {
        if (!welcomeMessageShown) {
            const welcomeText = "Hello, I am WildBot, your friendly virtual assistant. How can I assist you today? Whether you have questions, need information, or just want to chat, I'm here to help. Just type your query or request, and I'll do my best to provide you with the information and assistance you need.";
            displayBotMessage(welcomeText); // This function will append and also save to local storage
            welcomeMessageShown = true;
            localStorage.setItem('welcomeMessageShown', 'true');
        }
}

    // Function to load chat history from localStorage
    function loadChatHistory() {
        const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        chatMessages.empty();
        chatHistory.forEach(item => {
            const messageElement = $('<div></div>').addClass(item.role + '-message').text(item.message);
            chatMessages.append(messageElement);
        });
        scrollToBottom();
    }

    // Function to toggle chatpane visibility and load the latest chat history
    function toggleChatpane() {
        if (chatpane.is(":hidden")) {
            chatpane.fadeIn("medium", () => {
                loadChatHistory();
                scrollToBottom();
            });
            displayWelcomeMessage();
        } else {
            chatpane.fadeOut("medium");
        }
    }

    chatbotIcon.click(toggleChatpane);
    chatpaneHeader.click(toggleChatpane);

    // Function to display user messages in chatpane
    function displayUserMessage(message) {
        const userMessage = $('<div class="user-message"></div>').text(message);
        chatMessages.append(userMessage);
        scrollToBottom();
        saveMessageToStorage(message, 'user');
    }

    // Function to display bot messages in chatpane
    function displayBotMessage(message) {
        const botMessage = $('<div class="bot-message"></div>').text(message);
        chatMessages.append(botMessage);
        scrollToBottom();
        saveMessageToStorage(message, 'bot');
    }

    // Function to send and display messages
    function sendMessage() {
        const message = userInput.val().trim();
        if (message !== '') {
            displayUserMessage(message);
            $.ajax({
                url: '/chat',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'message': message }),
                success: function (data) {
                    displayBotMessage(data.response);
                },
                error: function () {
                    const errorMessage = "Sorry, the chat service is currently unavailable.";
                    displayBotMessage(errorMessage);
                }
            });
            userInput.val('');
        }
    }

    userInput.on('keyup', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    sendButton.click(sendMessage);

    // Function to clear chat history
    function clearChatHistory() {
        localStorage.removeItem('chatHistory');
        chatMessages.empty();
        welcomeMessageShown = false; // Reset the welcome message flag
        localStorage.setItem('welcomeMessageShown', 'false');
    }

    clearChatButton.click(function() {
        // Show modal here instead of confirm dialog
        showConfirmationModal();
    });

    // Function to show confirmation modal
    function showConfirmationModal() {
        $('#confirmation-modal').fadeIn('medium');

    }

    // Function to hide confirmation modal
    function hideConfirmationModal() {
        $('#confirmation-modal').fadeOut('medium');

    }

    $('#close-modal').click(function() {
        hideConfirmationModal(); // This will hide the modal when the X (close) button is clicked
    });

    // Assuming you have buttons with these IDs in your confirmation modal
    $('#confirm-clear').click(function () {
        clearChatHistory();
        hideConfirmationModal();
    });

    $('#cancel-clear').click(function () {
        hideConfirmationModal();
    });

    // Function to save chat messages to localStorage
    function saveMessageToStorage(message, role) {
        let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        chatHistory.push({ message, role });
        const maxMessages = 50;
        if (chatHistory.length > maxMessages) {
            chatHistory = chatHistory.slice(chatHistory.length - maxMessages);
        }
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }

    // Load and display chat history when the page loads
    loadChatHistory();
    scrollToBottom(); // Ensure the last message is shown on load
});