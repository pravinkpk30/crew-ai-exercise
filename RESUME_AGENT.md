# Resume Agent Documentation

## Overview
`resume-agent.py` is a Streamlit-based application that leverages CrewAI to create an AI-powered resume tailoring and interview preparation tool. It uses multiple AI agents to analyze job postings, enhance resumes, and generate interview preparation materials.

## Features
- **Job Posting Analysis**: Extracts key requirements from job postings
- **Profile Compilation**: Creates comprehensive professional profiles from GitHub and personal write-ups
- **Resume Tailoring**: Customizes resumes to match job requirements
- **Interview Preparation**: Generates relevant interview questions and talking points

## Agents and Their Roles

### 1. Tech Job Researcher
- **Purpose**: Analyzes job postings to identify key requirements
- **Tools Used**: Web scraping and search tools
- **Output**: Structured list of job requirements including skills, qualifications, and experiences

### 2. Personal Profiler
- **Purpose**: Creates detailed professional profiles
- **Tools Used**: Web scraping, resume parsing, and semantic search
- **Output**: Comprehensive profile document with skills, experiences, and contributions

### 3. Resume Strategist
- **Purpose**: Tailors resumes to match job requirements
- **Tools Used**: Resume parsing and semantic search
- **Output**: Updated resume highlighting relevant qualifications

### 4. Interview Preparer
- **Purpose**: Creates interview questions and talking points
- **Tools Used**: Resume parsing and semantic search
- **Output**: Customized interview preparation materials

## Prerequisites
- Python 3.8+
- Streamlit
- CrewAI
- Required API keys:
  - SERPER_API_KEY (for search functionality)
  - GOOGLE_API_KEY (for Gemini model access)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd crew-ai-exercise
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   # Linux/macOS
   export SERPER_API_KEY='your_serper_api_key_here'
   export GOOGLE_API_KEY='your_google_api_key_here'
   
   # Windows
   set SERPER_API_KEY=your_serper_api_key_here
   set GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

### Running the Application
1. Start the Streamlit application:
   ```bash
   streamlit run resume-agent.py
   ```

2. The application will open in your default web browser at `http://localhost:8501`

### Using the Application
1. **Input Fields**:
   - **Job Posting URL**: Paste the URL of the job posting you're applying for
   - **GitHub URL**: Your GitHub profile URL
   - **Personal Write-up**: A brief summary of your background and skills
   - **Resume**: Upload your current resume (PDF or DOCX)

2. **Process**:
   - The agents will analyze the job posting and your profile
   - Your resume will be tailored to match the job requirements
   - Custom interview questions and talking points will be generated

3. **Output**:
   - A tailored version of your resume
   - A list of potential interview questions
   - Talking points for your interview

## Customization
You can modify the agents' behavior by adjusting their parameters in the code:
- Change the LLM model
- Adjust the tools each agent uses
- Modify the task descriptions and expected outputs

## Troubleshooting
- **API Key Errors**: Ensure all required API keys are set in your environment variables
- **File Upload Issues**: Make sure the resume file is not password protected
- **Connection Errors**: Check your internet connection and API key validity

## Dependencies
- streamlit
- crewai
- python-dotenv
- PyPDF2 (for PDF resume parsing)
- python-docx (for DOCX resume parsing)

## License
[Specify your license here]

## Contributing
[Your contribution guidelines here]