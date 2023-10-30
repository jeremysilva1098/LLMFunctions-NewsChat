// Grabbing DOM elements
var userInput = document.getElementById('userInput');
var sendButton = document.getElementById('sendButton');
var messagesDiv = document.getElementById('messages');
sendButton.addEventListener('click', function () {
    var userMessage = userInput.value.trim();
    if (userMessage) {
        // Append user's message
        var userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'message user-msg';
        userMsgDiv.textContent = userMessage;
        messagesDiv.appendChild(userMsgDiv);
        // Add "thinking" message
        var thinkingMsgDiv_1 = document.createElement('div');
        thinkingMsgDiv_1.className = 'message thinking-msg';
        thinkingMsgDiv_1.textContent = 'NewsChat is going out and gathering news for you. Please wait...';
        messagesDiv.appendChild(thinkingMsgDiv_1);
        // Make an API call
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: "user_message=".concat(encodeURIComponent(userMessage))
        }).then(function (response) { return response.json(); })
            .then(function (data) {
            // Remove "thinking" message
            messagesDiv.removeChild(thinkingMsgDiv_1);
            var botMsgDiv = document.createElement('div');
            botMsgDiv.className = 'message sys-msg';
            botMsgDiv.textContent = data.response;
            messagesDiv.appendChild(botMsgDiv);
            if (data.citations.length > 0) {
                var citationsMsgDiv = document.createElement('div');
                citationsMsgDiv.className = 'message citations-msg';
                //citationsMsgDiv.textContent = 'Citations: ' + data.citations.join(', ');
                citationsMsgDiv.innerHTML = data.citations;
                messagesDiv.appendChild(citationsMsgDiv);
            }
        });
    }
    // Clear the input
    userInput.value = '';
});
