<!DOCTYPE html>
<html>
            <head>
                <title>Linux Shell by MalikShoaib</title>
                <style>
                    body {
                        background-color: #1a1a1a;
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        width: 100%;
                    }

                    h1 {
                        text-align: center;
                        margin-top: 50px;
                        color: white;
                    }

                    #chat-container {
                        display: flex;
                        flex-direction: column;
                        height: 80vh;
                        justify-content: flex-end;
                        align-items: center;
                        margin: 0 auto;
                        max-width: 800px;
                        padding: 20px;
                        background-color: gray;
                        border-radius: 20px;
                    }

                    #chat-input {
                        width: 80%;
                        height: 40px;
                        font-size: 16px;
                        padding: 10px;
                        border: none;
                        border-radius: 20px;
                        transition: all 0.3s ease;
                    }

                    #chat-input:focus {
                        outline: none;
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
                    }

                    #chat-btn {
                        width: 20%;
                        height: 40px;
                        font-size: 16px;
                        border: none;
                        border-radius: 20px;
                        background-color: #333;
                        color: white;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    }

                    #chat-btn:hover {
                        background-color: #555;
                    }

                    #chat-output {
                        width: 100%;
                        height: auto;
                        max-height: 60vh;
                        overflow-y: auto;
                        font-size: 16px;
                        padding: 10px;
                        border-radius: 20px;
                        background-color : white;
                        color: white;
                        margin-bottom: 20px;
                    }

                    .command {
                        color: #007bff;
                        font-weight: bold;
                    }

                    .output {
                        color: #28a745;
                    }

                    @media screen and (max-width: 768px) {
                        #chat-container {
                            width: 100%;
                        }

                        #chat-input {
                            width: 70%;
                        }

                        #chat-btn {
                            width: 30%;
                        }
                    }
                </style>
            </head>
            <body>
                <h1>Linux Shell by MalikShoaib</h1>
                <div id="chat-container">
                    <div id="chat-output"></div>
                    <div style="display: flex; width: 100%;">
                        <input id="chat-input" type="text" placeholder="Enter command...">
                        <button id="chat-btn">Send</button>
                    </div>
                </div>
                <script>
                    const chatInput = document.querySelector('#chat-input');
                    const chatBtn = document.querySelector('#chat-btn');
                    const chatOutput = document.querySelector('#chat-output');

                    function sendCommand(command) {
                        fetch('/shell/execute?command=' + encodeURIComponent(command))
                            .then(response => response.json())
                            .then(data => {
                                const commandElement = document.createElement('div');
                                commandElement.classList.add('command');
                                commandElement.innerHTML = command + '<br>';
                                chatOutput.appendChild(commandElement);

                                const outputElement = document.createElement('div');
                                outputElement.classList.add('output');
                                outputElement.innerHTML = data.output.replace('\\n', '<br>');
                                chatOutput.appendChild(outputElement);
                            });
                    }

                    chatBtn.addEventListener('click', function() {
                        const command = chatInput.value.trim();
                        if (command !== '') {
                            sendCommand(command);
                            chatInput.value = '';
                        }
                    });

                    chatInput.addEventListener('keyup', function(event) {
                        if (event.keyCode === 13) {
                            chatBtn.click();
                        }
                    });
                </script>
            </body>
        </html>
