Of course. Here is the complete Markdown content for your `README.md` file, ready to be copied and pasted.


# 📄 AI Resume Analyzer

An intelligent tool that analyzes your resume against a job description, providing a detailed match report, AI-powered suggestions, and links to learning resources for missing skills. This project leverages the Google Gemini API to deliver a smart, agentic analysis.

---

### **Live Demo**: [**ai-resume-analyser-fz5b.onrender.com**](https://ai-resume-analyser-fz5b.onrender.com/)

### **Google Colab Notebook**: [**Open in Colab**](https://colab.research.google.com/drive/18mYupGH0i-xdN0Uwyt8VvUUWvqsqodM6?usp=sharing)

---

## ✨ Features

-   **Technical Skill Matching**: Calculates a percentage score based on how your resume's technical skills match the job requirements.
-   **AI-Powered Suggestions**: Receives specific, actionable advice from the Gemini AI on how to improve your resume.
-   **Visual Analysis**: Displays a nested donut chart for an at-a-glance understanding of your skill breakdown.
-   **Learning Resources**: Automatically generates links to YouTube, Udemy, and Coursera tutorials for any missing technical skills.
-   **Soft Skill Identification**: Recognizes and lists required soft skills to help you prepare for interviews.
-   **Supports UN SDG #8**: Aligns with the Sustainable Development Goal for "Decent Work and Economic Growth" by helping job seekers improve their employability.

---

## 🤖 Agentic Workflow

The application operates as an intelligent agent. The Python environment acts as the "body" to handle files and tools, while the Gemini model acts as the "brain" to perform analysis and generate insights.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'background': '#FFFFFF'}}}%%
graph TD
    subgraph "User & Python Environment"
        A[User Input<br/>- Resume.pdf<br/>- JD.pdf] --> B{Python Environment}
        B -->|1.Extracts Text| C[Tool: PyMuPDF<br/>→ Raw Text]
    end

    subgraph "The Agentic Core"
        C -->|2.Sends Goal & Data| D[🧠 Gemini Agent]
        D -->|Plan:<br/>Analyze, Categorize, Compare, Suggest| E[Structured JSON<br/>- Skill Data<br/>- AI Suggestions]
    end

    subgraph "Final Assembly & Output"
        E -->|3.Executes Tasks| F[Tools:<br/>Matplotlib, Urllib<br/>→ Chart & Links]
        F -->|4.Assembles Report| G[Final Output:<br/>Chart, Report, Links]
    end

    style A fill:#E3F2FD,stroke:#90CAF9
    style B fill:#FFFDE7,stroke:#FFD54F
    style C fill:#E8F5E9,stroke:#81C784
    style D fill:#EDE7F6,stroke:#9575CD,stroke-width:3px
    style E fill:#FFF3E0,stroke:#FFB74D
    style F fill:#E8F5E9,stroke:#81C784
    style G fill:#D1F2EB,stroke:#4DB6AC,stroke-width:2px
````

-----

## 🚀 How to Run Locally

1.  **Clone the repository:**

    ```bash
    git clone [<your-repo-url>](https://github.com/u-8d/ai-resume-analyser)
    cd ai-resume-analyser
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**
    Create a `.env` file in the root directory and add your Gemini API key:

    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

4.  **Run the application:**

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:7860`.

-----

## ☁️ Deployment

This application is deployed as a Web Service on [Render](https://render.com/). The deployment process is configured as follows:

  - **Runtime**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python app.py`
  - **Environment Variable**: The `GEMINI_API_KEY` is set securely in the Render dashboard.

<!-- end list -->

```
```



