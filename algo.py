from skill import skill_set, skills
def score_resume(resume_data):
    score = 0
    
    # Adjusting experience weight: Reduce the score for experience to decrease bias
    experience_years = resume_data['experience']['Total Experience (years)']
    if experience_years >= 5:
        score += 15  # Reduced from 20
    elif 2 <= experience_years < 5:
        score += 10  # Reduced from 15
    elif 1 <= experience_years < 2:
        score += 7   # Reduced from 10
    else:
        score += 5   # Unchanged for less than 1 year

    
    candidate_skills = set(resume_data['Skills'])
    matching_skills = set(skills) & candidate_skills
    score += len(matching_skills) * 2  

      

    # Increasing the disparity in GPA scoring
    education_data = resume_data['Education']
    if 'GPA/CGPA' in education_data:
        gpa = float(education_data['GPA/CGPA'][0])
        if gpa >= 9:
            score += 20  # Higher emphasis on GPA 9+
        elif 8 <= gpa < 9:
            score += 12  # Slightly higher for 8 to 9 GPA
        elif 7 <= gpa < 8:
            score += 6   # Lower score for 7-8 GPA
        else:
            score += 2   # Minimal points for GPA below 7

    # Graduation year score remains the same
    graduation_year = education_data['Graduation Year'][0]
    if graduation_year != "Graduation Year Not Found":
        score += 5

    # Bonus for leadership/teamwork remains the same
    if 'Teamwork' in candidate_skills or 'Leadership' in candidate_skills:
        score += 5
    
    # Return the final score with adjusted weightings
    return score

def generate_course_url(skill, platform='udemy'):
    """
    Generate course URLs for different platforms like Udemy, Coursera, etc.
    """
    course_urls = {
        'udemy': f'https://www.udemy.com/courses/search/?q={skill}',
        'coursera': f'https://www.coursera.org/search?query={skill}',
        'linkedin': f'https://www.linkedin.com/learning/search?keywords={skill}',
        'youtube': f'https://www.youtube.com/results?search_query={skill}+tutorial'
    }
    return course_urls.get(platform, '')

def recommend_skills_and_courses(parsed_resume):
    recommendations = {}

    candidate_skills = set(parsed_resume['Skills'])

    best_fit_jobs = []
    missing_skills_for_best_fit = set()

    for job_role, required_skills in skill_set.items():
        job_missing_skills = set(required_skills) - candidate_skills

        match_percentage = len(candidate_skills & set(required_skills)) / len(required_skills) * 100
        if match_percentage >= 30:  
            best_fit_jobs.append({
                'Job Role': job_role,
                'Match Percentage': f"{match_percentage:.2f}%",
                'Missing Skills': list(job_missing_skills)
            })

            missing_skills_for_best_fit.update(job_missing_skills)

    if best_fit_jobs:
        recommendations['Best Fit Job Roles'] = best_fit_jobs
    else:
        recommendations['Best Fit Job Roles'] = ['No strong job match found.']

    course_recommendations = []
    for skill in missing_skills_for_best_fit:
        courses = {
            'Udemy': generate_course_url(skill, platform='udemy'),
            'Coursera': generate_course_url(skill, platform='coursera'),
            'LinkedIn Learning': generate_course_url(skill, platform='linkedin'),
            'YouTube': generate_course_url(skill, platform='youtube')
        }
        course_recommendations.append({
            'skill': skill,
            'courses': courses
        })

    if missing_skills_for_best_fit:
        recommendations['Missing Skills to Improve for Best Fit'] = list(missing_skills_for_best_fit)
        recommendations['Recommended Courses'] = course_recommendations
    else:
        recommendations['Missing Skills to Improve for Best Fit'] = ['No missing skills!']

    return recommendations