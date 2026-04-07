const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('frontend'));

// Store current chatbot process state
let chatbotProcess = null;
let conversationContext = [];

// Initialize chatbot and return initial greeting
app.post('/api/chat', (req, res) => {
    const { message, strategy } = req.body;

    if (!message) {
        return res.status(400).json({ error: 'Message required' });
    }

    // Spawn Python chatbot with chosen strategy
    const pythonScript = path.join(__dirname, 'chatbot.py');
    
    // Pass conversation context and strategy as arguments
    const args = [pythonScript, `--strategy=${strategy || 'zero-shot'}`, `--message=${message}`];
    
    const chatbot = spawn('python', args, {
  env: { ...process.env }  // pass Node’s environment to Python
});
    
    let output = '';
    let errorOutput = '';

    chatbot.stdout.on('data', (data) => {
        output += data.toString();
    });

    chatbot.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    chatbot.on('close', (code) => {
        if (code !== 0) {
            console.error('Python error:', errorOutput);
            return res.status(500).json({ error: 'Chatbot error: ' + errorOutput });
        }

        // Parse output (bot strips "bot: " prefix)
        const botResponse = output.replace('bot: ', '').trim();
        
        res.json({
            success: true,
            response: botResponse,
            context: conversationContext
        });
    });

    // Send user input to Python process
    chatbot.stdin.write(message + '\n');
    chatbot.stdin.end();
});

// Endpoint to reset conversation
app.post('/api/reset', (req, res) => {
    conversationContext = [];
    res.json({ success: true, message: 'Conversation reset' });
});

app.listen(PORT, () => {
    console.log(`ABC Restaurant Chatbot Server running on http://localhost:${PORT}`);
});
