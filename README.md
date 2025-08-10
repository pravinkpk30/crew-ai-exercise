# AI-Powered Resume Tailoring and Interview Preparation

This project is an AI-powered application that helps job seekers tailor their resumes and prepare for interviews using CrewAI. The application analyzes job postings, enhances resumes, and generates personalized interview preparation materials.

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - A fast Python package installer and resolver
- API Keys:
  - SERPER_API_KEY (for search functionality)
  - GOOGLE_API_KEY (for Gemini model access)

## Installation

### 1. Install uv

uv is a fast Python package installer and resolver, written in Rust. Install it using one of the following methods:

#### Using curl (macOS/Linux)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Using Homebrew (macOS)
```bash
brew install uv
```

#### Using PowerShell (Windows)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Clone the Repository
```bash
git clone <repository-url>
cd crew-ai-exercise
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
```bash
# .env
SERPER_API_KEY=your_serper_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## Running the Application

### 1. Install Dependencies
Use uv to install the required Python packages:

```bash
uv pip install -r requirements.txt
```

### 2. Start the Application
Run the Streamlit application using uv:

```bash
uv run streamlit run resume-agent.py
```

This will:
1. Create a virtual environment (if it doesn't exist)
2. Install all dependencies
3. Start the Streamlit development server

### 3. Access the Application
Once the server starts, you can access the application in your web browser at:
```
http://localhost:8501
```

## Usage

1. **Input Your Information**:
   - Paste the job posting URL
   - Enter your GitHub profile URL
   - Provide a personal write-up about your background
   - Upload your current resume

2. **Let the AI Work**:
   - The application will analyze the job posting
   - Your resume will be tailored to match the job requirements
   - Custom interview questions and talking points will be generated

3. **Review and Download**:
   - Review the tailored resume
   - Study the generated interview questions
   - Download the materials for your job application

## Development

### Installing Development Dependencies
```bash
uv pip install -r requirements-dev.txt
```

### Running Tests
```bash
uv run pytest tests/
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**
   - Ensure both `SERPER_API_KEY` and `GOOGLE_API_KEY` are set in your `.env` file

2. **Package Installation Issues**
   - Try clearing the uv cache: `uv pip cache clean`
   - Then reinstall: `uv pip install -r requirements.txt`

3. **Port Already in Use**
   - If port 8501 is in use, you can specify a different port:
     ```bash
     uv run streamlit run resume-agent.py --server.port=8502
     ```

## License
[Specify your license here]

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.