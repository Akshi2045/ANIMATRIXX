import os
import re
import subprocess
import sys
from llm_client import generate_manim_code, extract_python_code, save_code_to_file

def find_manim_class_name(code: str) -> str:
    """Scans the generated Python code using Regex to find the name of the Manim Scene class."""
    pattern = r"class\s+(\w+)\s*\(\s*\w*Scene\w*\s*\)\s*:"
    match = re.search(pattern, code)
    if match:
        return match.group(1)
    
    pattern_fallback = r"class\s+(\w+)\s*\("
    match_fallback = re.search(pattern_fallback, code)
    if match_fallback:
        return match_fallback.group(1)
        
    return "ExpandingBlueCircle"  # Default fallback

def run_manim_rendering(filepath: str, class_name: str) -> bool:
    """Executes the Manim compiler command as a Python subprocess."""
    print(f"\n [Rendering] Compiling class {class_name} from {filepath}...")
    # -p: preview video when finished, -ql: low quality (renders fast at 480p)
    command = ["manim", "-pql", filepath, class_name]
    
    try:
        result = subprocess.run(command, check=True)
        if result.returncode == 0:
            print("\n [Rendering Success] Animation generated and opened successfully!")
            return True
    except subprocess.CalledProcessError as e:
        print(f"\n [Rendering Error] Manim compilation failed: {e}")
    except FileNotFoundError:
        print(f"\n [System Error] 'manim' command not found. Ensure Manim is installed and accessible.")
    return False

def start_pipeline():
    print("==========================================================")
    print("                FULL AUTOMATION PIPELINE                  ")
    print("                 AI ANIMATION PLATFORM                    ")
    print("==========================================================")
    
    user_prompt = input("\nWhat educational animation would you like to build? ")
    if not user_prompt.strip():
        print("Empty input. Running default physics demo...")
        user_prompt = "Animate a projectile motion trajectory with a bouncing ball."
        
    raw_response = generate_manim_code(user_prompt)
    if not raw_response:
        print("[Error] Failed to get response from Gemini.")
        return
        
    clean_code = extract_python_code(raw_response)
    scene_file = "generated_scene.py"
    save_code_to_file(clean_code, scene_file)
    
    class_name = find_manim_class_name(clean_code)
    print(f" [Parser] Detected generated Scene class name: {class_name}")
    
    run_manim_rendering(scene_file, class_name)

if __name__ == "__main__":
    start_pipeline()