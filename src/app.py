import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
import subprocess
import streamlit as st
from llm_client import generate_manim_code, extract_python_code, save_code_to_file
def find_manim_class_name(code: str) -> str:
    """Scans the generated code to find the Scene class name."""
    pattern = r"class\s+(\w+)\s*\(\s*\w*Scene\w*\s*\)\s*:"
    match = re.search(pattern, code)
    if match:
        return match.group(1)
    return "DynamicScene"

def render_manim_video(filepath: str, class_name: str):
    """Renders the Manim scene into an MP4 video (without popping up a local player)."""
    # We use -ql (low quality, fast) or -qm (medium quality). No '-p' flag!
    command = ["manim", "-ql", filepath, class_name]
    
    with st.spinner("🎬 Manim engine is drawing your animation frames..."):
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            st.error(f"Manim Compiler Error:\n{e.stderr}")
            return False

# --- STREAMLIT UI LAYOUT ---
st.set_page_config(page_title="AI Educational Animator", page_icon="🧮", layout="wide")

st.title("🧮 AI Educational Animation Platform")
st.subheader("Turn simple text ideas into beautiful mathematical animations using Gemini & Manim")

# Create a two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Define Your Animation")
    user_prompt = st.text_area(
        "What concepts or shapes would you like to animate?",
        placeholder="e.g., Draw an X and Y axis, plot a red parabola (y = x^2), and label the vertex.",
        height=150
    )
    
    generate_btn = st.button("Generate & Render Animation", type="primary")

with col2:
    st.header("2. Video Output")
    
    if generate_btn:
        if not user_prompt.strip():
            st.warning("Please enter a prompt first!")
        else:
            # Step 1: Query Gemini
            with st.spinner("🤖 Consulting Gemini for optimal code logic..."):
                raw_response = generate_manim_code(user_prompt)
            
            if raw_response:
                clean_code = extract_python_code(raw_response)
                scene_file = "generated_scene.py"
                save_code_to_file(clean_code, scene_file)
                
                class_name = find_manim_class_name(clean_code)
                
                # Step 2: Render via Manim Subprocess
                success = render_manim_video(scene_file, class_name)
                
                if success:
                    # Step 3: Locate the output file and display it
                    # Manim's default directory structure: media/videos/generated_scene/480p15/ClassName.mp4
                    video_path = f"media/videos/generated_scene/480p15/{class_name}.mp4"
                    
                    if os.path.exists(video_path):
                        st.success("✨ Animation successfully generated!")
                        st.video(video_path)
                    else:
                        st.error("Video file was generated but could not be located in the project directory paths.")
                        
                # Optional: Display the code under the video
                with st.expander("👁️ View Generated Python Source Code"):
                    st.code(clean_code, language="python")
            else:
                st.error("Failed to retrieve code from the AI model. Check your API key or network connection.")