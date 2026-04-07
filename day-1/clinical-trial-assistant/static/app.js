const pdfInput = document.getElementById('pdfInput');
const fileNameDisplay = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

// Typing Indicator HTML
const typingHtml = `
<div class="typing-indicator" id="typingIndicator" style="display:flex;">
    <span></span><span></span><span></span>
</div>
`;

let selectedFile = null;

// File Selection
pdfInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        fileNameDisplay.textContent = selectedFile.name;
        uploadBtn.disabled = false;
    }
});

// Upload process
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Processing...";
    uploadStatus.textContent = "";
    uploadStatus.className = "status-message";

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            uploadStatus.textContent = `Success! Processed ${data.chunks} segments.`;
            questionInput.disabled = false;
            sendBtn.disabled = false;
            addMessage(`Document "${selectedFile.name}" has been loaded and indexed. You can now ask questions about it.`, 'system-msg');
        } else {
            throw new Error(data.detail || "Upload failed.");
        }
    } catch (error) {
        uploadStatus.textContent = error.message;
        uploadStatus.className = "status-message error";
        uploadBtn.disabled = false;
    } finally {
        uploadBtn.textContent = "Process Document";
    }
});

function addMessage(text, type, citations = []) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    
    let citationsHtml = '';
    if (citations && citations.length > 0) {
        citationsHtml = '<div class="citations-container">';
        citations.forEach(c => {
            citationsHtml += `
                <div class="citation-block">
                    <strong>📄 Source: ${c.source}</strong>
                    "${c.content}"
                </div>`;
        });
        citationsHtml += '</div>';
    }

    msgDiv.innerHTML = `
        <div class="msg-content">
            ${text.replace(/\n/g, '<br>')}
        </div>
        ${citationsHtml}
    `;
    
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    chatMessages.insertAdjacentHTML('beforeend', typingHtml);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

// Chat Process
async function handleSend() {
    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, 'user-msg');
    questionInput.value = '';
    questionInput.disabled = true;
    sendBtn.disabled = true;

    showTyping();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        removeTyping();

        if (response.ok) {
            addMessage(data.answer, 'assistant-msg', data.citations);
        } else {
            addMessage(`Error: ${data.detail}`, 'system-msg');
        }
    } catch (error) {
        removeTyping();
        addMessage(`Connection error: ${error.message}`, 'system-msg');
    } finally {
        questionInput.disabled = false;
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

sendBtn.addEventListener('click', handleSend);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});
