import requests
from pdfminer.high_level import extract_text
import re
from typing import List, Dict
from skill import skills
import os
import spacy
from spacy.matcher import Matcher
from datetime import datetime



nlp = spacy.load('en_core_web_sm')



def extract_text_from_pdf(pdf_path: str) -> str:
    return extract_text(pdf_path)





def extract_name(resume_text: str) -> str:

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}], 
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  
    ]
    
    for pattern in patterns:
        matcher.add('NAME', [pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text  
    return "Name not found"

def extract_contact_number_from_resume(text: str) -> str:
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_contact_number_from_resume(text: str) -> str:
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else "Contact Number Not Found"


def extract_email_from_resume(text: str) -> str:
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else "Email Not Found"

def extract_skills_from_resume(text: str) -> list[str]:
    found_skills = []
    text = text.lower()  
    for skill in skills:
        if skill.lower() in text: 
            found_skills.append(skill)
    
    return found_skills if found_skills else ["No skills found"]

def extract_experience(text: str) -> Dict[str, any]:
    experience = {}
    
    # Extracting job titles (common titles, add more based on your needs)
    job_title_pattern = r"(Software Engineer|Intern|Developer|Consultant|Analyst|Manager|Lead|Engineer|Intern|Software Developer)"
    job_titles = re.findall(job_title_pattern, text, re.IGNORECASE)
    
    # Extracting periods (Start Date - End Date) or (Start Date - Present)
    date_pattern = r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{4})\s*[-–]\s*(\b(?:Present|\d{4})\b)"
    date_matches = re.findall(date_pattern, text)
    
    experiences_list = []
    total_experience_years = 0
    
    for i, (start_date, end_date) in enumerate(date_matches):
        start_date_obj = datetime.strptime(start_date, "%b %Y")
        if end_date.lower() == "present":
            end_date_obj = datetime.now()
        else:
            end_date_obj = datetime.strptime(end_date, "%Y")
        
        # Calculating the difference in years
        experience_years = (end_date_obj - start_date_obj).days / 365.25
        total_experience_years += experience_years
        
        # Store job title and dates
        job_title = job_titles[i] if i < len(job_titles) else "Unknown"
        experiences_list.append({
            "Job Title": job_title,
            "Start Date": start_date,
            "End Date": end_date,
            "Experience (years)": round(experience_years, 2)
        })
    
    experience['Total Experience (years)'] = round(total_experience_years, 2)
    experience['Job Details'] = experiences_list
    return experience


def extract_education_from_resume(text: str) -> Dict[str, any]:
    education_details = {}


    degree_pattern = r"(?i)\b(?:B(?:\.?E|\.?Tech|achelor)|M(?:\.?E|\.?Tech|aster)|Ph\.?D|Diploma|Doctorate)\b(?:\s(?:of|in)?\s*\w+)?"
    degree_matches = re.findall(degree_pattern, text)
    education_details['Degree'] = list(set(degree_matches)) if degree_matches else ["Degree Not Found"]

    university_pattern = r"(?i)(?:\b(?:University|Institute|College|School|Academy|Technology)\b\s*(?:\w+\s*)+)"
    university_matches = re.findall(university_pattern, text)
    education_details['University/College'] = list(set(university_matches)) if university_matches else ["University/College Not Found"]

    gpa_pattern = r"(?:CGPA|SGPA|GPA)[^0-9]{0,3}(\d\.\d{1,2})"
    gpa_matches = re.findall(gpa_pattern, text)
    education_details['GPA/CGPA'] = list(set(gpa_matches)) if gpa_matches else ["CGPA/SGPA Not Found"]

    year_pattern = r"(\d{4})\s*[-–]\s*(\d{4})|\bGraduated(?: in)?\s*(\d{4})"
    year_matches = re.findall(year_pattern, text)
    year_extracted = []
    for match in year_matches:
        if match[0] and match[1]:
            year_extracted.append(f"{match[0]}-{match[1]}")
        elif match[2]:
            year_extracted.append(match[2])
    education_details['Graduation Year'] = year_extracted if year_extracted else ["Graduation Year Not Found"]

    return education_details

def parse_resume(pdf_path: str) -> Dict[str, any]:
    text = extract_text_from_pdf(pdf_path)
    
    name = extract_name(text)
    contact_number = extract_contact_number_from_resume(text)
    email = extract_email_from_resume(text)
    skills = extract_skills_from_resume(text)
    education = extract_education_from_resume(text)
    experience = extract_experience(text)

    return {
        'Name': name,
        'Contact Number': contact_number,
        'Email': email,
        'Skills': skills,
        'Education': education,
        'experience' : experience,
    }


def parse_job_description(jd_text: str) -> Dict[str, any]:
    # Extract job title
    job_title_pattern = r"Job Title[:\s]*([A-Za-z\s]+)"
    job_title_match = re.search(job_title_pattern, jd_text)
    job_title = job_title_match.group(1).strip() if job_title_match else "Job Title Not Found"
    
    # Extract company name
    company_pattern = r"(Company|Organization)[:\s]*([A-Za-z0-9\s]+)"
    company_match = re.search(company_pattern, jd_text)
    company_name = company_match.group(2).strip() if company_match else "Company Name Not Found"
    
    # Extract location (generalized for common terms)
    location_pattern = r"(Location|Work Location|Office):?[\s]*([A-Za-z0-9\s,]+)"
    location_match = re.search(location_pattern, jd_text)
    location = location_match.group(2).strip() if location_match else "Location Not Found"
    
    # Extract duration (for internships, full-time, part-time)
    duration_pattern = r"(Duration|Employment Type|Term):?[\s]*([A-Za-z0-9\s]+)"
    duration_match = re.search(duration_pattern, jd_text)
    duration = duration_match.group(2).strip() if duration_match else "Duration Not Found"
    
    # Extract job description skills from skill.py
    found_skills = []
    jd_lower = jd_text.lower()  # Lowercasing the JD text to make matching case-insensitive
    for skill in skills:
        if skill.lower() in jd_lower:
            found_skills.append(skill)
    
    # Extract qualifications and requirements (generalizing for multiple patterns)
    qualifications_pattern = r"(Qualifications|Requirements):?\s*(.*?)(\n\s*\n|\n\s*[A-Z])"
    qualifications_match = re.search(qualifications_pattern, jd_text, re.DOTALL)
    qualifications = qualifications_match.group(2).strip() if qualifications_match else "Qualifications Not Found"
    
    # Extract roles and responsibilities (generalizing for multiple patterns)
    roles_pattern = r"(Roles And Responsibilities|Job Responsibilities|Key Responsibilities):?\s*(.*?)(\n\s*\n|\n\s*[A-Z])"
    roles_match = re.search(roles_pattern, jd_text, re.DOTALL)
    roles = roles_match.group(2).strip() if roles_match else "Roles and Responsibilities Not Found"
    
    # Extract any deadlines or application dates
    deadline_pattern = r"(Deadline|Apply by):?\s*(.*?)(\n|\r)"
    deadline_match = re.search(deadline_pattern, jd_text)
    deadline = deadline_match.group(2).strip() if deadline_match else "Deadline Not Found"
    
    # Extract company overview or other sections (generalizing further)
    other_info_pattern = r"(Company Overview|About Us|What We Offer):?\s*(.*?)\n\n"
    other_info_matches = re.findall(other_info_pattern, jd_text, re.DOTALL)
    other_info = {section: content.strip() for section, content in other_info_matches}
    
    return {
        "Job Title": job_title,
        "Company Name": company_name,
        "Location": location,
        "Duration": duration,
        "Skills": found_skills if found_skills else ["No relevant skills found"],
        "Qualifications": qualifications,
        "Roles and Responsibilities": roles,
        "Deadline": deadline,
        "Other Information": other_info
    }