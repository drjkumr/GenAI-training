from graph_engine import chatbot_graph
import os

def generate_graph_viz():
    print("Attempting to generate graph visualization...")
    try:
        # Generate the graph as a mermaid string
        mermaid_code = chatbot_graph.get_graph().draw_mermaid()
        
        # Save the mermaid code to a file
        with open("workflow_graph.mermaid", "w", encoding="utf-8") as f:
            f.write(mermaid_code)
        print("SUCCESS: Mermaid workflow code saved to 'workflow_graph.mermaid'")
        
        # Try to save as PNG if libraries are installed
        try:
            png_data = chatbot_graph.get_graph().draw_mermaid_png()
            with open("workflow_graph.png", "wb") as f:
                f.write(png_data)
            print("SUCCESS: Graph image saved to 'workflow_graph.png'")
        except Exception as e:
            print("INFO: Could not generate PNG (requires extra dependencies).")
            print("   You can paste the content of 'workflow_graph.mermaid' into https://mermaid.live to see the graph.")
            
    except Exception as e:
        print(f"ERROR generating graph: {e}")

if __name__ == "__main__":
    generate_graph_viz()
