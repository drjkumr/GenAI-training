# ABC South Indian Restaurant Chatbot - Implementation Guide

## Quick Start

This project demonstrates three prompting strategies for a customer support chatbot using Claude Haiku.

### Prerequisites
- Node.js 14+ 
- Python 3.8+
- Anthropic API key (get from https://console.anthropic.com)

### Installation & Setup

#### 1. Backend Setup
```bash
cd backend
npm install
```

#### 2. Add Your API Key
Create/edit `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

#### 3. Install Python Dependencies
```bash
pip install anthropic python-dotenv
```

#### 4. Start the Backend Server
```bash
# From backend directory
npm start
```

Expected output:
```
ABC Restaurant Chatbot Server running on http://localhost:3000
```

#### 5. Open in Browser
Navigate to: `http://localhost:3000`

## How to Use

1. **Select a Prompting Strategy** from the dropdown:
   - **Zero-Shot**: Single prompt, no examples
   - **Few-Shot**: Includes example conversations
   - **Chain-of-Thought**: Step-by-step reasoning

2. **Ask Questions** about:
   - Menu items
   - Prices
   - Recommendations
   - Availability

3. **Reset Chat** to clear conversation history

## Menu Reference

### Food Items (Rs. 150 each)
- Plain Dosa
- Rava Dosa
- Onion Rava Dosa
- Idli
- Pongal
- Kesari
- Sambhar Vada
- Curd Vada
- Utphappam
- Idiyappam

### Drinks
- Hot Drinks (Rs. 25): Tea, Coffee, Hot Milk, Hot Chocolate
- Juices (Rs. 80): Orange, Sweet Lime, Apple, Grape

## Testing the Strategies

**Good Test Queries:**
- "What's on the menu?"
- "How much is a dosa?"
- "Do you have pizza?"
- "What do you recommend?"
- "What's the cost of 2 idlis and 1 tea?"
- "Recommend something for Rs. 200"
- "Compare the dosas"

## File Structure
```
abc-restaurant-chatbot/
├── backend/
│   ├── chatbot.py              # Python chatbot (unmodified)
│   ├── server.js               # Express API server
│   ├── package.json            # Node dependencies
│   └── .env                    # API key (add yours here)
├── frontend/
│   └── index.html              # Chat UI
└── README.md                   # This file
```

## Architecture

```
Frontend (Fetch API) 
    ↓
Express.js Server (localhost:3000)
    ↓
Python Chatbot + Anthropic API
```

### How It Works
1. User types in browser
2. Frontend sends POST to `/api/chat`
3. Backend spawns Python chatbot process
4. Python sends request to Claude Haiku
5. Response returned to frontend and displayed

## Troubleshooting

### Port 3000 Already in Use
```bash
# Use a different port by editing server.js PORT variable
```

### "Cannot find module 'cors'"
```bash
npm install cors
```

### "ANTHROPIC_API_KEY not found"
- Verify `.env` file exists in `backend/`
- Check format: `ANTHROPIC_API_KEY=sk-ant-...`

### Python not found
```bash
# Ensure Python is in your PATH or use full path
C:\Python39\python.exe backend/chatbot.py
```

## Learn More

See `chatbot-prompt-strategies.md` for:
- Full system prompts for each strategy
- Example conversations
- Detailed approach explanations
- Performance comparisons

## Model Used
**claude-haiku-4-5-20251001** - Fast, efficient, perfect for customer support

---

**Created:** April 2026  
**Purpose:** Prompt Engineering & AI Design Education
