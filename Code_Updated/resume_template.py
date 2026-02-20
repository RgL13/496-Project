import pandas as pd
import random

names = pd.read_csv("names.csv")

job_templates = {
    "data_scientist": {
        "education": "BS in Statistics",
        "experience": "Data Analyst Intern at a mid-size tech company; built regression and classification models in Python and presented findings to stakeholders.",
        "research": "Co-authored a research paper on machine learning model interpretability; performed cross-validation and statistical evaluation.",
        "gpa": "3.8"
    },

    "software_engineer": {
        "education": "BS in Computer Science",
        "experience": "Software Engineering Intern; developed backend APIs in Python and improved application performance by 15%.",
        "research": "Designed and implemented a machine learning model for a senior capstone project using real-world datasets.",
        "gpa": "3.7"
    },

    "business_analyst": {
        "education": "BS in Business Analytics",
        "experience": "Business Analyst Intern; performed SQL-based data extraction and created dashboard reports for management.",
        "research": "Conducted structured market research and competitor analysis for a startup expansion strategy.",
        "gpa": "3.6"
    },

    "lawyer": {
        "education": "JD in Law",
        "experience": "Legal Intern at a corporate law firm; assisted in drafting contracts and reviewing compliance documents.",
        "research": "Published a legal research paper on corporate governance and regulatory frameworks.",
        "gpa": "3.9"
    },

    "financial_advisor": {
        "education": "BS in Finance",
        "experience": "Finance Intern; performed valuation modeling and prepared financial projections using Excel.",
        "research": "Conducted quantitative financial analysis on startup capital structure and investment risk.",
        "gpa": "3.7"
    },

    "hr_assistant": {
        "education": "BA in Psychology",
        "experience": "HR Assistant; supported recruitment screening and organized onboarding processes for new hires.",
        "research": "Conducted survey-based research on employee satisfaction and workplace engagement trends.",
        "gpa": "3.4"
    },

    "product_manager": {
        "education": "BS in Information Systems",
        "experience": "Product Management Intern; coordinated cross-functional teams and drafted product requirement documents (PRDs).",
        "research": "Led a data-driven product development project analyzing user behavior and feature prioritization.",
        "gpa": "3.8"
    },

    "doctor": {
        "education": "BS in Biology",
        "experience": "Clinical Research Assistant; supported patient data collection and assisted in laboratory experiments.",
        "research": "Co-authored a research paper evaluating treatment outcomes using statistical analysis.",
        "gpa": "3.9"
    },

    "consulting_analyst": {
        "education": "BS in Economics",
        "experience": "Consulting Intern; conducted industry benchmarking and built financial forecasting models.",
        "research": "Performed applied economic analysis for a local business expansion case study.",
        "gpa": "3.7"
    },

    "nursing": {
        "education": "BA in Nursing",
        "experience": "Nursing Intern in a hospital setting; assisted with patient monitoring and clinical documentation.",
        "research": "Participated in applied research on patient care protocols and healthcare efficiency.",
        "gpa": "3.5"
    }
}

jobs_df = pd.DataFrame.from_dict(job_templates, orient="index")
jobs_df.reset_index(inplace=True)
jobs_df.rename(columns={"index": "job_title"}, inplace=True)

resumes_df = names.merge(jobs_df, how="cross")

# print("Total resumes:", len(resumes_df))  

resumes_df["resume"] = resumes_df.apply(
    lambda row: f"""Job Applied: {row['job_title']}
Education: {row['education']}
Experience: {row['experience']}
Research: {row['research']}
GPA: {row['gpa']}""",
    axis=1
)

job_initials = {
    "data_scientist": "DS",
    "software_engineer": "SE",
    "business_analyst": "BA",
    "lawyer": "L",
    "financial_advisor": "FA",
    "hr_assistant": "HR",
    "product_manager": "PM",
    "doctor": "D",
    "consulting_analyst": "CA",
    "nursing": "N"
}

resumes_df["job_seq"] = resumes_df.groupby("job_title").cumcount() + 1

resumes_df["resume_id"] = resumes_df.apply(
    lambda row: f"{job_initials[row['job_title']]}{row['job_seq']:02}",
    axis=1
)

resumes_df = resumes_df.sample(frac=1, random_state=123).reset_index(drop=True)


resumes_df = resumes_df[[
    "resume_id",
    "full_name",
    "race",
    "gender",
    "job_title",
    "resume"
]]

resumes_df.to_csv("resumes.csv", index=False)

# print("Saved resumes.csv")
