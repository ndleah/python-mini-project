import gradio as gr
import fitz
import google.generativeai as genai
import json
import matplotlib.pyplot as plt
import time
import numpy as np
from urllib.parse import quote
import os

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file, limited to the first 5 pages."""
    if not pdf_file: return ""
    try:
        doc = fitz.open(pdf_file.name)
        text = "".join(page.get_text() for page_num, page in enumerate(doc) if page_num < 5)
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def analyze_with_gemini(resume_text, jd_text):
    """
    Analyzes documents with the fast and efficient Gemini 1.5 Flash model.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return False, "Error: GEMINI_API_KEY environment variable not set on the server."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""
        You are a top-tier senior recruiter and career coach with 15 years of experience. Your task is to conduct a deep analysis of a resume against a job description.

        1.  From the job description, meticulously extract the core "jd_technical_skills" (e.g., Python, AWS, React) and "jd_soft_skills" (e.g., Leadership, Communication).
        2.  From the resume, extract all "resume_technical_skills" you can discern.
        3.  Critically compare the resume to the job description and generate a list of 2-4 highly specific, actionable "suggestions" for improving the resume. These suggestions must be insightful and go beyond simple keyword matching. For example: "The job requires 'Terraform' for infrastructure management. Your resume mentions AWS but not specific IaC tools. Consider adding a bullet point under your cloud project detailing how you automated infrastructure provisioning, even if you used a different tool."
        4.  IMPORTANT: Discard vague, non-skill phrases. Be discerning.
        5.  Return a single, clean JSON object with four keys: "jd_technical_skills", "jd_soft_skills", "resume_technical_skills", and "suggestions".

        Resume Text:
        ---
        {resume_text}
        ---

        Job Description Text:
        ---
        {jd_text}
        ---

        Provide only the raw JSON object in your response.
        """

        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        parsed_json = json.loads(cleaned_response)

        jd_technical = set(skill.lower() for skill in parsed_json.get("jd_technical_skills", []))
        jd_soft = set(skill.lower() for skill in parsed_json.get("jd_soft_skills", []))
        resume_technical = set(skill.lower() for skill in parsed_json.get("resume_technical_skills", []))
        suggestions = parsed_json.get("suggestions", [])

        return True, (jd_technical, jd_soft, resume_technical, suggestions)

    except Exception as e:
        return False, f"Gemini API Error: {str(e)}. The model may have returned an unexpected format. Please try again."

def get_learning_resources(missing_skills):
    """
    Generates a markdown string with links to learning resources for missing skills.
    """
    if not missing_skills:
        return ""
    links_md = "## 📚 Learning Resources\nHere are some links to help you get started on the missing technical skills:\n\n"
    for skill in sorted(list(missing_skills)):
        query = quote(f"{skill} tutorial for beginners")
        udemy_query = quote(skill)
        links_md += f"### {skill.title()}\n* [Search on YouTube](https://www.youtube.com/results?search_query={query})\n* [Search on Udemy](https://www.udemy.com/courses/search/?q={udemy_query})\n* [Search on Coursera](https://www.coursera.org/search?query={udemy_query})\n\n"
    return links_md

def create_pie_chart(matched_count, missing_count):
    """Generates a clean pie chart with a white background."""
    if matched_count == 0 and missing_count == 0:
        return None

    labels = ['Matched Technical Skills', 'Missing Technical Skills']
    sizes = [matched_count, missing_count]
    colors = ['#2E8B57', '#CD5C5C']
    explode = (0.1, 0) if matched_count > 0 else (0, 0)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('white')
    ax.patch.set_facecolor('white')

    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=140,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    plt.setp(autotexts, size=14, weight="bold", color="white")
    plt.setp(texts, size=12, weight="bold", color="#333333")
    ax.axis('equal')
    ax.set_title('Technical Skill Match', fontsize=16, fontweight='bold', pad=20)
    
    filepath = f"/tmp/skill_chart_{int(time.time())}.png"
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    return filepath


def analyze_documents(resume_pdf, jd_pdf, progress=gr.Progress()):
    """Orchestrates the analysis process and generates the report and chart."""
    if not resume_pdf or not jd_pdf:
        return None, "Please upload both your Resume and the Job Description."
    
    # Check for API key at the start of the process
    if not os.environ.get('GEMINI_API_KEY'):
         return None, "🔴 **Configuration Error**: The application's API key is not set on the server. Please contact the administrator."

    progress(0, desc="Starting Analysis...")
    progress(0.2, desc="Extracting text from PDFs...")
    resume_text = extract_text_from_pdf(resume_pdf)
    jd_text = extract_text_from_pdf(jd_pdf)

    progress(0.4, desc="Analyzing documents with Gemini Flash...")
    success, data = analyze_with_gemini(resume_text, jd_text)
    if not success:
        return None, f"Analysis Failed: {data}"

    jd_technical, jd_soft, resume_technical, suggestions = data
    if not jd_technical:
        return None, "Analysis failed: Gemini could not identify any required technical skills in the Job Description."

    progress(0.7, desc="Calculating score and generating visuals...")
    matched_technical = resume_technical.intersection(jd_technical)
    missing_technical = jd_technical.difference(resume_technical)
    match_score = (len(matched_technical) / len(jd_technical)) * 100 if jd_technical else 0
    chart_path = create_pie_chart(len(matched_technical), len(missing_technical))

    progress(0.9, desc="Finding learning resources...")
    learning_links_md = get_learning_resources(missing_technical)

    # --- Build the Report ---
    result = f"# ⭐ Resume Analysis Report\n\n"
    result += f"Your resume has a **{match_score:.1f}%** match with the job's **core technical requirements**.\n\n"
    result += f"## 💡 AI-Powered Suggestions\n\n"
    if suggestions:
        for suggestion in suggestions:
            result += f"- {suggestion}\n"
    else:
        result += "No specific suggestions were generated. Your resume looks well-aligned!"

    result += f"\n\n---\n"
    result += f"## ✅ Matched Technical Skills ({len(matched_technical)})\n"
    result += ", ".join(sorted([s.title() for s in matched_technical])) if matched_technical else "None"
    result += f"\n\n## ❌ Missing Technical Skills ({len(missing_technical)})\n"
    result += ", ".join(sorted([s.title() for s in missing_technical])) if missing_technical else "None! Great job."
    result += f"\n\n---\n"
    result += f"### 💬 Required Soft Skills ({len(jd_soft)})\n"
    result += "While not part of the score, be prepared to discuss these:\n\n"
    result += ", ".join(sorted([s.title() for s in jd_soft])) if jd_soft else "None specified."
    result += f"\n\n---\n{learning_links_md}"
    result += "\n\n*Powered by Google Gemini 1.5 Flash. This is an automated guide.*"

    progress(1, desc="Done!")
    return chart_path, result

# --- GRADIO UI ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue"), css=".gradio-container {max-width: 1280px !important}") as iface:
    gr.Markdown("# 📄 AI Resume Analyzer")
    gr.Markdown("Get an instant, intelligent analysis of your resume against a job description. Powered by Google Gemini 1.5 Flash.")

    with gr.Row(variant='panel'):
        with gr.Column(scale=1, min_width=350):
            gr.Markdown("### 1. Upload Documents")
            resume_file = gr.File(label="Your Resume (PDF)")
            jd_file = gr.File(label="Job Description (PDF)")
            analyze_btn = gr.Button("Analyze Resume", variant="primary", scale=2)

        with gr.Column(scale=2):
            gr.Markdown("### 2. Analysis Results")
            output_report = gr.Markdown(label="Analysis Report")

    with gr.Row():
        with gr.Column():
             gr.Markdown("### 3. Match Visualization")
             output_chart = gr.Image(label="Technical Skills Match", show_label=False, interactive=False)


    analyze_btn.click(
        fn=analyze_documents,
        inputs=[resume_file, jd_file],
        outputs=[output_chart, output_report],
        api_name="analyze"
    )
iface.launch(server_name="0.0.0.0", server_port=7860)
