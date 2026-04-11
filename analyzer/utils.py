import PyPDF2
import re

def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_sections(text):
    result = {}

    # Name - first line
    lines = text.strip().split('\n')
    result["name"] = lines[-1].strip()

    # Skills - between TECHNICAL SKILLS and PROJECTS
    skills_match = re.search(
        r'TECHNICAL SKILLS\s*(.*?)\s*PROJECTS',
        text, re.DOTALL
    )

    if skills_match:
        raw_skills = skills_match.group(1)
        # split by comma, newline, or common separators
        skills_list = re.split(r'[,\n]', raw_skills)
        # clean each one
        cleaned = []
        for skill in skills_list:
            skill = skill.strip().lower()
            # remove long lines like "programming languages python"
            # keep only short clean skill names
            if 1 < len(skill) < 25:
                cleaned.append(skill)
        result["skills"] = ", ".join(cleaned)
    else:
        result["skills"] = ""

    # Projects - between PROJECTS and EDUCATION
    projects_match = re.search(
        r'PROJECTS\s*(.*?)\s*EDUCATION',
        text, re.DOTALL
    )
    result["projects"] = projects_match.group(1).strip() if projects_match else ""

    return result