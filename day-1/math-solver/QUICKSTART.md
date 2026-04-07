# Quick Start Guide

Get the math solver running in under 5 minutes.

## Prerequisites Check

```bash
# Verify Node.js is installed
node --version
npm --version

# You need Node.js 18+ and npm 9+
```

## Step 1: Install Dependencies

```bash
cd backend
npm install
```

**What this does:**
- Installs Express (web framework)
- Installs Anthropic SDK (API client)
- Installs CORS (cross-origin support)
- Installs TypeScript compiler

## Step 2: Create .env File

In the `backend/` folder, create a file named `.env`:

```
ANTHROPIC_API_KEY=sk-ant-v7-YOUR_ACTUAL_KEY_HERE
PORT=3001
```

**To get your API key:**
1. Go to https://console.anthropic.com
2. Click "API Keys" in the left sidebar
3. Create a new API key
4. Copy it and paste into `.env`

## Step 3: Build Backend

```bash
cd backend
npm run build
```

This compiles TypeScript to JavaScript.

## Step 4: Start Backend

```bash
npm start
```

You should see:
```
✓ Math Solver Backend running on http://localhost:3001
✓ Model: claude-haiku-4-5-20251001
✓ API Key configured: Yes
```

## Step 5: Start Frontend (New Terminal)

```bash
cd frontend

# Option A: Using Python (usually pre-installed)
python -m http.server 3000

# Option B: Using Node (if you have http-server installed)
npx http-server -p 3000

# Option C: VS Code - Right-click index.html → Open with Live Server
```

## Step 6: Open in Browser

Visit: **http://localhost:3000**

You should see the Math Solver interface.

## Test It

Try these example problems:

1. **Simple arithmetic:**
   - "What is 25% of 80?"
   - "Calculate 15 × 12"

2. **Algebra:**
   - "Solve: 2x + 5 = 15"
   - "What is x if 3x - 7 = 20?"

3. **Word problems:**
   - "If a book costs $15 and is on sale for 20% off, how much will you pay?"
   - "A train travels 60 mph for 2.5 hours. How far does it go?"

## Troubleshooting

### "Cannot GET /solve"
- Backend is not running. Run `npm start` in the backend folder.

### "Invalid API key"
- Check that `ANTHROPIC_API_KEY` in `.env` is correct and not empty.
- Try using a fresh API key from the Anthropic console.

### CORS errors
- Make sure frontend is on `localhost:3000` and backend is on `localhost:3001`.
- Backend has CORS enabled by default.

### "Problem field is required"
- You must enter a math problem before clicking "Solve Problem".

## Files Modified

After setup, your folder should look like:

```
math-solver/
├── backend/
│   ├── node_modules/          (created by npm install)
│   ├── dist/                  (created by npm run build)
│   ├── src/
│   │   └── server.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── .env                   (YOUR API KEY HERE)
├── frontend/
│   └── index.html
├── .env.example
└── README.md
```

## Next Steps

- The backend can be deployed to Heroku, Railway, or Fly.io
- The frontend can be deployed to Vercel, Netlify, or GitHub Pages
- To add more features, modify `server.ts` for backend logic or `index.html` for frontend UI

## Model Information

- **Model Used:** `claude-haiku-4-5-20251001`
- **Max Tokens:** 1024 (per request)
- **Speed:** Very fast (suitable for real-time responses)
- **Cost:** Most affordable Claude model

For API pricing: https://www.anthropic.com/pricing/claude
