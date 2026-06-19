# 🧮 AI Educational Animation Platform (Animatrix)

An automated, end-to-end Python pipeline that converts descriptive text prompts into mathematical and educational animations. The platform leverages the **Google GenAI SDK** to generate strict, syntactically guardrailed **Manim (Community Edition)** code, compiles it programmatically via a subprocess pipeline, and embeds the output into an interactive web dashboard built with **Streamlit**.

## Features
- **Intelligent LLM Bridge:** Integrates Google's `gemini-2.5-flash` model with customized system guardrails to eliminate common runtime compilation errors (e.g., zero-width textures, incorrect vector comparisons).
- **Subprocess Rendering Engine:** Programmatically executes and captures localized Manim rendering workflows in real-time.
- **Modern Web UI:** Features a multi-column Streamlit interface that accepts prompts, manages async background compilation states, and embeds interactive HTML5 video players for instant preview.

##  Architecture & Tech Stack
- **Language:** Python 3.12+
- **AI Core:** Google GenAI SDK (`gemini-2.5-flash`)
- **Animation Framework:** Manim Community Edition
- **Web Frontend:** Streamlit Framework
- **Environment Management:** Python `venv`, `python-dotenv`

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Akshi2045/ANIMATRIX.git](https://github.com/Akshi2045/ANIMATRIX.git)
   cd ANIMATRIX