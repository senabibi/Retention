import os
import json
import glob
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize API clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def process_prompt(content):
    """Process different prompt formats and return the full prompt string"""
    if "Input" in content and "Question" in content:
        # Baseline or Summary-Aided format
        filler = content.get("Long filler text", "")
        return f"{content['Input']}\n\n{filler}\n\n{content['Question']}"
    elif "Needle" in content and "Steps" in content:
        # Multi-Step Forgetting format
        return f"{content['Needle']}\n\n" + "\n".join(content["Steps"]) + f"\n\n{content['Question']}"
    elif "Stage 1" in content:
        # Prompt Chaining format
        return "\n\n".join([content[stage] for stage in sorted(content.keys()) if stage.startswith("Stage")])
    else:
        raise ValueError("Unknown prompt format")

def call_api(model, prompt):
    """Make API calls to the specified model"""
    try:
        if model == "gpt4":
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=1000
            )
            return response.choices[0].message.content
        elif model == "claude3":
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240607",  # Updated to latest version
                max_tokens=1000,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
    except Exception as e:
        return f"API_ERROR: {str(e)}"

def run_experiment(file_path):
    """Process a single JSON file and return results"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load {file_path}: {str(e)}"}

    # Handle both dictionary and list formats
    if isinstance(data, list):
        data = {f"Prompt_{i+1}": item for i, item in enumerate(data)}
    
    results = {}
    for prompt_id, content in data.items():
        try:
            prompt = process_prompt(content)
            results[prompt_id] = {
                "prompt": prompt,
                "gpt4": call_api("gpt4", prompt),
                "claude3": call_api("claude3", prompt),
                "expected_answer": content.get("expected_answer", "NOT_PROVIDED")
            }
        except Exception as e:
            results[prompt_id] = {
                "error": f"Failed to process {prompt_id}: {str(e)}"
            }
    return results

def main():
    """Main execution function"""
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)

    # Process all JSON files in the data directory
    json_files = glob.glob("data/*.json")
    
    for file_path in json_files:
        print(f"\nProcessing: {file_path}")
        results = run_experiment(file_path)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            continue
        
        output_file = f"results/{os.path.basename(file_path).replace('.json', '')}_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()