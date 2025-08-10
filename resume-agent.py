import streamlit as st
import os
import tempfile


# Import CrewAI components
from crewai import Agent, Task, Crew, LLM
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)


os.environ['SERPER_API_KEY'] = "YOUR_SERPER_KEY"


# Check if API keys are set (optional, but good for user feedback)
if os.environ['SERPER_API_KEY'] == "YOUR_SERPER_API_KEY_HERE":
    st.warning("API keys not found.")
    st.stop()


def run_job_application_crew(job_posting_url: str, github_url: str, personal_writeup: str, resume_file_path: str):
    """
    Runs the CrewAI job application crew with the given inputs.

    Args:
        job_posting_url (str): URL of the job posting.
        github_url (str): GitHub profile URL of the applicant.
        personal_writeup (str): Personal write-up/summary of the applicant.
        resume_file_path (str): Path to the uploaded resume file.

    Returns:
        tuple: (tailored_resume_content, interview_materials_content)
    """

    # Initialize LLM
    llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
        max_tokens=1024
    )


    # Initialize tools with the uploaded resume path
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    read_resume = FileReadTool(file_path=resume_file_path)

    # The MDXSearchTool needs to be re-initialized for the specific uploaded file
    # Note: mdx_nlp_semantic_search==0.0.4 is required for MDXSearchTool to work correctly
    semantic_search_resume = MDXSearchTool(
        mdx=resume_file_path,
        config=dict(
            embedder=dict(
                provider="huggingface",
                config=dict(
                    model="sentence-transformers/all-MiniLM-L6-v2"
                ),
            ),
        ),
    )

    # Agent 1: Researcher
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Make sure to do amazing analysis on "
             "job posting to help job applicants",
        tools = [scrape_tool, search_tool],
        verbose=True,
        backstory=(
            "As a Job Researcher, your prowess in "
            "navigating and extracting critical "
            "information from job postings is unmatched."
            "Your skills help pinpoint the necessary "
            "qualifications and skills sought "
            "by employers, forming the foundation for "
            "effective application tailoring."
        ),
        llm=llm
    )

    # Agent 2: Profiler
    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Do incredible research on job applicants "
             "to help them stand out in the job market",
        tools = [scrape_tool, search_tool,
                 read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "Equipped with analytical prowess, you dissect "
            "and synthesize information "
            "from diverse sources to craft comprehensive "
            "personal and professional profiles, laying the "
            "groundwork for personalized resume enhancements."
        ),
        llm=llm
    )

    # Agent 3: Resume Strategist
    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Find all the best ways to make a "
             "resume stand out in the job market.",
        tools = [scrape_tool, search_tool,
                 read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "With a strategic mind and an eye for detail, you "
            "excel at refining resumes to highlight the most "
            "relevant skills and experiences, ensuring they "
            "resonate perfectly with the job's requirements."
        ),
        llm=llm
    )

    # Agent 4: Interview Preparer
    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Create interview questions and talking points "
             "based on the resume and job requirements",
        tools = [scrape_tool, search_tool,
                 read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "Your role is crucial in anticipating the dynamics of "
            "interviews. With your ability to formulate key questions "
            "and talking points, you prepare candidates for success, "
            "ensuring they can confidently address all aspects of the "
            "job they are applying for."
        ),
        llm=llm
    )

    # Task for Researcher Agent: Extract Job Requirements
    research_task = Task(
        description=(
            f"Analyze the job posting URL provided ({job_posting_url}) "
            "to extract key skills, experiences, and qualifications "
            "required. Use the tools to gather content and identify "
            "and categorize the requirements."
        ),
        expected_output=(
            "A structured list of job requirements, including necessary "
            "skills, qualifications, and experiences."
        ),
        agent=researcher,
        async_execution=True
    )

    # Task for Profiler Agent: Compile Comprehensive Profile
    profile_task = Task(
        description=(
            f"Compile a detailed personal and professional profile "
            f"using the GitHub ({github_url}) URLs, and personal write-up "
            f"({personal_writeup}). Utilize tools to extract and "
            "synthesize information from these sources."
        ),
        expected_output=(
            "A comprehensive profile document that includes skills, "
            "project experiences, contributions, interests, and "
            "communication style."
        ),
        agent=profiler,
        async_execution=True
    )

    # Task for Resume Strategist Agent: Align Resume with Job Requirements
    resume_strategy_task = Task(
        description=(
            "Using the profile and job requirements obtained from "
            "previous tasks, tailor the resume to highlight the most "
            "relevant areas. Employ tools to adjust and enhance the "
            "resume content. Make sure this is the best resume even but "
            "don't make up any information. Update every section, "
            "inlcuding the initial summary, work experience, skills, "
            "and education. All to better reflrect the candidates "
            "abilities and how it matches the job posting."
        ),
        expected_output=(
            "An updated resume that effectively highlights the candidate's "
            "qualifications and experiences relevant to the job."
        ),
        output_file="tailored_resume.md",
        context=[research_task, profile_task],
        agent=resume_strategist
    )

    # Task for Interview Preparer Agent: Develop Interview Materials
    interview_preparation_task = Task(
        description=(
            "Create a set of potential interview questions and talking "
            "points based on the tailored resume and job requirements. "
            "Utilize tools to generate relevant questions and discussion "
            "points. Make sure to use these question and talking points to "
            "help the candiadte highlight the main points of the resume "
            "and how it matches the job posting."
        ),
        expected_output=(
            "A document containing key questions and talking points "
            "that the candidate should prepare for the initial interview."
        ),
        output_file="interview_materials.md",
        context=[research_task, profile_task, resume_strategy_task],
        agent=interview_preparer
    )


    job_application_crew = Crew(
        agents=[researcher,
                profiler,
                resume_strategist,
                interview_preparer],

        tasks=[research_task,
               profile_task,
               resume_strategy_task,
               interview_preparation_task],

        verbose=True,
        max_rpm=2
    )

    job_application_inputs = {
        'job_posting_url': job_posting_url,
        'github_url': github_url,
        'personal_writeup': personal_writeup
    }

    # Execute the crew
    try:
        with st.spinner("Running CrewAI... This might take a few minutes as agents perform their tasks."):
            job_application_crew.kickoff(inputs=job_application_inputs)

        # Read the generated files
        with open("tailored_resume.md", "r") as f:
            tailored_resume_content = f.read()

        with open("interview_materials.md", "r") as f:
            interview_materials_content = f.read()

        return tailored_resume_content, interview_materials_content

    except Exception as e:
        st.error(f"An error occurred during CrewAI execution: {e}")
        return None, None
    finally:
        # Clean up generated files
        if os.path.exists("tailored_resume.md"):
            os.remove("tailored_resume.md")
        if os.path.exists("interview_materials.md"):
            os.remove("interview_materials.md")


# --- Streamlit UI ---
st.set_page_config(page_title="AI-Powered Resume Tailor & Interview Prep", layout="wide")

st.title("🚀 AI-Powered Resume Tailor & Interview Prep")
st.markdown("""
Upload your resume, provide job details, and let CrewAI generate a
tailored resume and interview questions to help you land your dream job!
""")

st.header("1. Upload Your Resume")
uploaded_file = st.file_uploader("Choose a Markdown (.md) resume file", type="md")

st.header("2. Provide Job & Personal Details")
col1, col2 = st.columns(2)

with col1:
    job_url = st.text_input(
        "Job Posting URL"
    )
with col2:
    github_url = st.text_input(
        "GitHub Profile URL"
    )

personal_writeup = st.text_area(
    "Personal Summary/Write-up",
    height=150
)

st.markdown("---")

if st.button("✨ Generate Tailored Resume & Interview Prep", type="primary"):
    if uploaded_file is None:
        st.error("Please upload your resume (.md file) to proceed.")
    elif not job_url or not github_url or not personal_writeup:
        st.error("Please fill in all the job and personal details.")
    else:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            resume_temp_path = tmp_file.name

        try:
            tailored_resume, interview_materials = run_job_application_crew(
                job_url, github_url, personal_writeup, resume_temp_path
            )

            if tailored_resume and interview_materials:
                st.success("Generation Complete!")

                st.header("3. Tailored Resume")
                st.download_button(
                    label="Download Tailored Resume",
                    data=tailored_resume,
                    file_name="tailored_resume.md",
                    mime="text/markdown"
                )
                st.markdown("---") # Separator
                st.subheader("Preview of Tailored Resume:")
                st.markdown(tailored_resume)


                st.header("4. Interview Preparation Materials")
                st.download_button(
                    label="Download Interview Materials",
                    data=interview_materials,
                    file_name="interview_materials.md",
                    mime="text/markdown"
                )
                st.markdown("---") # Separator
                st.subheader("Preview of Interview Materials:")
                st.markdown(interview_materials)

        finally:
            # Clean up the temporary resume file
            if os.path.exists(resume_temp_path):
                os.remove(resume_temp_path)
