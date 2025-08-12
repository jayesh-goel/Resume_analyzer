// Event listener for the form submission
document.getElementById("resumeForm").addEventListener("submit", handleResumeSubmission);

async function handleResumeSubmission(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById("resumeFile");
    const file = fileInput.files[0];
    const resultSection = document.getElementById("result");
    
    // Validate file input
    if (!file) {
        showError("Please select a file to upload.");
        return;
    }
    
    // Validate file type
    if (file.type !== 'application/pdf') {
        showError("Please upload a PDF file only.");
        return;
    }
    
    try {
        // Show loading state
        toggleLoadingState(true);
        
        // Upload and process the resume
        const result = await uploadResume(file);
        console.log("Backend Response:", result);
        
        // Display results
        displayResults(result);
    } catch (error) {
        console.error("Error processing resume:", error);
        showError("Failed to process resume. Please try again later.");
    } finally {
        toggleLoadingState(false);
    }
}

async function uploadResume(file) {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await fetch("http://localhost:8000/process-resume/", {
        method: "POST",
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

function displayResults(result) {
    const resultSection = document.getElementById("result");
    resultSection.style.display = "block";
    
    // Display resume score
    document.getElementById("score").textContent = result["Resume Score"];
    
    // Display job roles
    displayJobRoles(result.Recommendations["Best Fit Job Roles"]);
    
    // Display missing skills
    displayMissingSkills(result.Recommendations["Missing Skills"]);
    
    // Display recommended courses
    displayRecommendedCourses(result.Recommendations["Recommended Courses"]);
}

function displayJobRoles(roles) {
    const jobRolesList = document.getElementById("jobRoles");
    jobRolesList.innerHTML = "";
    
    roles.forEach(role => {
        const li = document.createElement("li");
        li.textContent = `${role["Job Role"]} - Match: ${role["Match Percentage"]}%`;
        jobRolesList.appendChild(li);
    });
}

function displayMissingSkills(skills) {
    const missingSkillsList = document.getElementById("missingSkills");
    missingSkillsList.innerHTML = "";
    
    skills.forEach(skill => {
        const li = document.createElement("li");
        li.textContent = skill;
        missingSkillsList.appendChild(li);
    });
}

function displayRecommendedCourses(courses) {
    const coursesList = document.getElementById("courses");
    coursesList.innerHTML = "";
    
    courses.forEach(course => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${escapeHtml(course.skill)}</strong>:
            <a href="${escapeHtml(course.courses.Udemy)}" target="_blank" rel="noopener noreferrer">Udemy</a>,
            <a href="${escapeHtml(course.courses.Coursera)}" target="_blank" rel="noopener noreferrer">Coursera</a>,
            <a href="${escapeHtml(course.courses.LinkedIn)}" target="_blank" rel="noopener noreferrer">LinkedIn Learning</a>,
            <a href="${escapeHtml(course.courses.YouTube)}" target="_blank" rel="noopener noreferrer">YouTube</a>
        `;
        coursesList.appendChild(li);
    });
}

function showError(message) {
    alert(message);
}

function toggleLoadingState(isLoading) {
    const submitButton = document.querySelector('#resumeForm button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = isLoading;
        submitButton.textContent = isLoading ? 'Processing...' : 'Submit';
    }
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}