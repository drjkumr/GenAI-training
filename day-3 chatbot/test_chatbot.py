from graph_engine import chatbot_graph
import os

# Clean up previous logs if any
if os.path.exists("menu_suggestions.txt"):
    os.remove("menu_suggestions.txt")

def load_kb():
    if os.path.exists("rag_knowledge_base.txt"):
        with open("rag_knowledge_base.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

kb = load_kb()

test_cases = [
    {
        "name": "Semantic Support (Closing Time)",
        "input": "When is the restaurant shut?",
        "expected_keywords": ["10:00 PM"]
    },
    {
        "name": "Menu Query (RAG)",
        "input": "How much for a Plain Dosa and Coffee?",
        "expected_keywords": ["150", "25"]
    },
    {
        "name": "Menu Suggestion (Routing)",
        "input": "You should definitely add Masala Dosa to your menu!",
        "expected_keywords": ["suggestion", "thank you", "improve"]
    }
]

def run_tests():
    results = []
    print("Running Chatbot Tests...")
    
    for case in test_cases:
        print(f"Testing: {case['name']}")
        
        # Mock the state
        state = {
            "messages": [{"role": "user", "content": case['input']}],
            "context": [{"role": "user", "content": case['input']}],
            "knowledge_base": kb
        }
        
        # Invoke graph
        try:
            final_state = chatbot_graph.invoke(state)
            response = final_state.get("response", "").lower()
            category = final_state.get("category", "")
            
            passed = all(kw.lower() in response for kw in case['expected_keywords'])
            
            res_str = f"Test Case: {case['name']}\n"
            res_str += f"Input: {case['input']}\n"
            res_str += f"Category: {category}\n"
            res_str += f"Response: {response}\n"
            res_str += f"Status: {'PASSED' if passed else 'FAILED'}\n"
            res_str += "-"*30 + "\n"
            results.append((passed, res_str))
            
        except Exception as e:
            res_str = f"Test Case: {case['name']} - ERROR: {e}\n"
            results.append((False, res_str))

    # Calculate Score
    score = sum(1 for p, _ in results if p) / len(results) * 10
    
    # Save to tests.txt
    with open("tests.txt", "w", encoding="utf-8") as f:
        f.write(f"CHATBOT TEST RESULTS\n")
        f.write(f"Overall Functionality Score: {score}/10\n\n")
        for _, text in results:
            f.write(text)
            
    # Check if suggestion was logged
    if os.path.exists("menu_suggestions.txt"):
        with open("menu_suggestions.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if "Masala Dosa" in content:
                print("Logging verified: Suggestion was saved to file.")

    print(f"Tests completed. Score: {score}/10. Results saved to tests.txt.")

if __name__ == "__main__":
    run_tests()
