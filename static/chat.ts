
// Grabbing DOM elements
const userInput: HTMLInputElement = <HTMLInputElement>document.getElementById('userInput');
const sendButton: HTMLElement = document.getElementById('sendButton');
const messagesDiv: HTMLElement = document.getElementById('messages');

sendButton.addEventListener('click', () => {
    let userMessage = userInput.value.trim();
    
    if (userMessage) {
        // Append user's message
        let userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'message user-msg';
        userMsgDiv.textContent = userMessage;
        messagesDiv.appendChild(userMsgDiv);

        // Add "thinking" message
        let thinkingMsgDiv = document.createElement('div');
        thinkingMsgDiv.className = 'message thinking-msg';
        thinkingMsgDiv.textContent = 'NewsChat is going out and gathering news for you. Please wait...';
        messagesDiv.appendChild(thinkingMsgDiv);

        // Make an API call
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_message=${encodeURIComponent(userMessage)}`
        }).then(response => response.json())
          .then(data => {
              // Remove "thinking" message
              messagesDiv.removeChild(thinkingMsgDiv);

              let botMsgDiv = document.createElement('div');
              botMsgDiv.className = 'message sys-msg';
              botMsgDiv.textContent = data.response;
              messagesDiv.appendChild(botMsgDiv);

              if (data.citations.length > 0) {
                let citationsMsgDiv = document.createElement('div');
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
