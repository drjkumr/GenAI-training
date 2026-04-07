# Simple Math Solver with Chain-of-Thought Reasoning

A minimal educational demo showing how a frontend sends math problems to a backend that uses Claude Haiku 4.5 to generate step-by-step solutions.

## Architecture Overview

```
math-solver/
├── backend/
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       └── server.ts          (single Express file, ~80 lines)
├── frontend/
│   └── index.html            (single HTML file, ~100 lines)
└── .env.example
```

## Quick Setup (< 30 minutes)

### 1. Prerequisites
- Node.js 18+ installed
- Anthropic API key (get one at https://console.anthropic.com)

### 2. Installation

```bash
# Create project folder
mkdir math-solver && cd math-solver

# Setup backend
mkdir -p backend/src
cd backend
npm init -y
npm install express cors typescript @types/express @types/node @anthropic-ai/sdk
npx tsc --init

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
EOF

cd ..

# Setup frontend (no dependencies needed)
mkdir frontend
```

### 3. Environment Setup

Create `.env` file in the backend folder:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
PORT=3001
```

### 4. Run

```bash
# Terminal 1: Start backend
cd backend
npx tsc && node dist/server.js

# Terminal 2: Open frontend
cd frontend
python -m http.server 3000
# OR: npx http-server -p 3000
# Then visit http://localhost:3000
```

## Key Features

- ✅ Single Express file (backend)
- ✅ Single HTML file (frontend)
- ✅ One API route: `POST /solve`
- ✅ Chain-of-thought reasoning prompt
- ✅ Exact model: `claude-haiku-4-5-20251001`
- ✅ Simple error handling
- ✅ No database, no classes, minimal architecture

## How It Works

1. **Frontend** sends a math problem as JSON to the backend
2. **Backend** receives the problem and calls Anthropic API
3. **Claude Haiku** generates step-by-step solution using chain-of-thought
4. **Frontend** displays the formatted response

## Example Request/Response

**Request to `/solve`:**
```json
{
  "problem": "What is 25% of 80?"
}
```

**Response:**
```json
{
  "problem": "What is 25% of 80?",
  "solution": "Let me solve this step-by-step...\nStep 1: Convert 25% to decimal: 25% = 0.25\nStep 2: Multiply 80 by 0.25...\nStep 3: 80 × 0.25 = 20\nAnswer: 25% of 80 is 20"
}
```
