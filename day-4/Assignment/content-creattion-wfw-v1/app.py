from flask import Flask, render_template_string, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# HTML Template with Tailwind CSS for a premium look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARM-Lite Agentic Pipeline</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background: #f8fafc; }
        .gradient-text { background: linear-gradient(90deg, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stage-card { transition: all 0.3s ease; }
        .stage-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); }
        .loading-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <header class="mb-12 text-center">
            <h1 class="text-4xl md:text-5xl font-extrabold mb-4 gradient-text">Smart Agent Workflow</h1>
            <p class="text-slate-500 text-lg">A High-Performance Agentic Pipeline Optimized for ARM64.</p>
        </header>

        <!-- Topic Input -->
        <div class="bg-white p-6 rounded-2xl shadow-sm mb-12 flex flex-col md:flex-row items-center gap-4">
            <input type="text" id="topic" value="AI Agentic Workflows 2024" 
                   class="flex-1 w-full p-4 text-lg rounded-xl border-slate-200 border-2 focus:ring-2 focus:ring-blue-400 focus:outline-none outline-none">
            <button onclick="resetAll()" class="bg-slate-100 px-6 py-4 rounded-xl font-semibold text-slate-600 hover:bg-slate-200 transition-colors">Reset</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Stage 1: Research -->
            <div id="card-1" class="stage-card bg-white p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col h-full">
                <div class="mb-6 flex items-center justify-between">
                    <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Step 1</span>
                    <div id="status-1" class="w-3 h-3 rounded-full bg-slate-200"></div>
                </div>
                <h2 class="text-2xl font-bold mb-4">🔍 Researcher</h2>
                <p class="text-slate-500 mb-8 flex-1">Identifies key trends, statistics, and industry insights for your topic.</p>
                <button id="btn-1" onclick="runStage(1)" class="w-full bg-blue-600 text-white py-4 rounded-xl font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-200">Run Research</button>
                <div id="result-1" class="mt-8 text-sm text-slate-700 whitespace-pre-wrap hidden bg-slate-50 p-4 rounded-xl max-h-60 overflow-y-auto"></div>
            </div>

            <!-- Stage 2: Write -->
            <div id="card-2" class="stage-card bg-white p-8 rounded-3xl shadow-sm border border-slate-100 opacity-50 flex flex-col h-full">
                <div class="mb-6 flex items-center justify-between">
                    <span class="bg-purple-100 text-purple-600 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Step 2</span>
                    <div id="status-2" class="w-3 h-3 rounded-full bg-slate-200"></div>
                </div>
                <h2 class="text-2xl font-bold mb-4">✍️ Writer</h2>
                <p class="text-slate-500 mb-8 flex-1">Crafts a compelling 500-word blog post using gathered insights.</p>
                <button id="btn-2" disabled onclick="runStage(2)" class="w-full bg-purple-600 text-white py-4 rounded-xl font-bold opacity-50 cursor-not-allowed transition-all">Write Content</button>
                <div id="result-2" class="mt-8 text-sm text-slate-700 whitespace-pre-wrap hidden bg-slate-50 p-4 rounded-xl max-h-60 overflow-y-auto"></div>
            </div>

            <!-- Stage 3: Review -->
            <div id="card-3" class="stage-card bg-white p-8 rounded-3xl shadow-sm border border-slate-100 opacity-50 flex flex-col h-full">
                <div class="mb-6 flex items-center justify-between">
                    <span class="bg-emerald-100 text-emerald-600 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Step 3</span>
                    <div id="status-3" class="w-3 h-3 rounded-full bg-slate-200"></div>
                </div>
                <h2 class="text-2xl font-bold mb-4">✅ Reviewer</h2>
                <p class="text-slate-500 mb-8 flex-1">Polishes grammar, tone, and accuracy for a professional finish.</p>
                <button id="btn-3" disabled onclick="runStage(3)" class="w-full bg-emerald-600 text-white py-4 rounded-xl font-bold opacity-50 cursor-not-allowed transition-all">Final Review</button>
                <div id="result-3" class="mt-8 text-sm text-slate-700 whitespace-pre-wrap hidden bg-slate-50 p-4 rounded-xl max-h-60 overflow-y-auto"></div>
            </div>
        </div>

        <!-- Final Export -->
        <div id="final-export" class="mt-12 hidden">
            <div class="bg-slate-900 text-white p-10 rounded-3xl shadow-2xl">
                <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
                    <span class="text-emerald-400">🏆</span> Final Polished Output
                </h3>
                <div id="final-content" class="text-slate-300 leading-relaxed max-h-96 overflow-y-auto mb-8 whitespace-pre-wrap"></div>
                <button onclick="download('final_blog.md')" class="bg-white text-slate-900 px-8 py-3 rounded-full font-bold hover:bg-slate-100 transition-colors">Download .md file</button>
            </div>
        </div>
    </div>

    <script>
        let results = { 1: '', 2: '', 3: '' };

        async function runStage(stage) {
            const topic = document.getElementById('topic').value;
            const btn = document.getElementById(`btn-${stage}`);
            const status = document.getElementById(`status-${stage}`);
            const resultBox = document.getElementById(`result-${stage}`);

            // UI Loading State
            btn.disabled = true;
            btn.innerText = 'Processing...';
            status.className = 'w-3 h-3 rounded-full bg-yellow-400 loading-pulse';

            try {
                const response = await fetch('/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stage, topic, context: results })
                });
                const data = await response.json();

                if (data.error) throw new Error(data.error);

                results[stage] = data.output;
                
                // Success State
                btn.innerText = 'Completed';
                btn.className = 'w-full bg-slate-100 text-slate-400 py-4 rounded-xl font-bold cursor-default';
                status.className = 'w-3 h-3 rounded-full bg-emerald-500';
                resultBox.innerText = data.output;
                resultBox.classList.remove('hidden');

                // Unlock next stage
                if (stage < 3) {
                    const nextCard = document.getElementById(`card-${stage + 1}`);
                    const nextBtn = document.getElementById(`btn-${stage + 1}`);
                    nextCard.classList.remove('opacity-50');
                    nextBtn.disabled = false;
                    nextBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                } else {
                    document.getElementById('final-export').classList.remove('hidden');
                    document.getElementById('final-content').innerText = data.output;
                }

            } catch (err) {
                alert(err.message);
                btn.disabled = false;
                btn.innerText = 'Retry';
                status.className = 'w-3 h-3 rounded-full bg-red-500';
            }
        }

        function download(filename) {
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(results[3]));
            element.setAttribute('download', filename);
            element.click();
        }

        function resetAll() {
            window.location.reload();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run', methods=['POST'])
def run_stage():
    data = request.json
    stage = data.get('stage')
    topic = data.get('topic')
    context = data.get('context', {})

    prompts = {
        1: {
            "sys": "You are an expert tech researcher. Provide a detailed summary of trends, stats, and key players for the given topic. Use a structural format with bullet points.",
            "user": f"Research the latest trends in: {topic}"
        },
        2: {
            "sys": "You are a creative blog writer. Use the research provided to write a compelling 500-word blog post. Use SEO-friendly headers and an engaging tone.",
            "user": f"Write a blog post based on this research:\n{context.get('1')}"
        },
        3: {
            "sys": "You are a senior editor. Review the draft for grammar, tone, and technical accuracy. Provide the FINAL polished version as the only output in Markdown format.",
            "user": f"Finalize this draft:\n{context.get('2')}"
        }
    }

    try:
        current = prompts.get(stage)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": current["sys"]},
                {"role": "user", "content": current["user"]}
            ],
            temperature=0.7
        )
        output = response.choices[0].message.content
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 ARM-Lite Agent Server starting at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
