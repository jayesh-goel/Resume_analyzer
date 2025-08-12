# 🤖 AI Resume Analyzer

An intelligent AI-powered resume analysis system that evaluates resumes, provides comprehensive scoring, and delivers personalized career recommendations! 🚀

## ⭐ Features

- 📄 **PDF Resume Processing**: Seamless upload and parsing of PDF resumes
- 🧠 **AI-Powered Scoring**: Multi-factor intelligent scoring algorithm based on:
  - Work experience analysis
  - Skills matching and relevance
  - Educational background and GPA
  - Leadership and teamwork indicators
- 🎯 **Smart Job Role Matching**: Advanced compatibility matching with percentage scores
- 🔍 **Skill Gap Analysis**: Identifies missing skills for target positions
- 📚 **Personalized Course Recommendations**: Curated learning paths from multiple platforms
- 🌐 **RESTful API**: Easy integration with FastAPI-based endpoints
- ⚡ **Real-time Processing**: Fast and efficient resume analysis
- 📊 **Comprehensive Reports**: Detailed analysis with actionable insights

## 🛠️ Technology Stack

- **Backend Framework**: 
  - FastAPI (High-performance async API)
  - Python 3.8+
  
- **AI/ML & NLP**:
  - spaCy for advanced natural language processing
  - Custom ML algorithms for scoring
  - PDF text extraction with pdfminer.six
  
- **Data Processing**:
  - Advanced regex pattern matching
  - Entity recognition and extraction
  - Skills database with 200+ technical skills

## 🔥 How It Works

1. **📤 Resume Upload**: Users upload PDF resumes through the API endpoint
2. **🔍 Text Extraction**: Advanced PDF parsing extracts clean text content
3. **🧠 NLP Processing**: 
   - spaCy processes text for entity recognition
   - Custom algorithms extract skills, experience, and education
   - Pattern matching identifies key resume components
4. **📊 Intelligent Scoring**: 
   - Experience weight: 5-15 points
   - Skills matching: 2 points per relevant skill
   - Academic performance: 2-20 points (GPA-based)
   - Leadership/teamwork: 5 bonus points
   - Education completeness: 5 points
5. **🎯 Job Role Matching**: Compares candidate profile with 20+ job role requirements
6. **💡 Smart Recommendations**: Generates personalized skill development and course suggestions

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### 🔧 Installation

1. **Clone the repository**
```bash
git clone 
cd ai-resume-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. **Launch the application**
```bash
uvicorn main:app --reload
```

5. **Access the API**
- 📖 Interactive API docs: `http://localhost:8000/docs`
- 📋 Alternative docs: `http://localhost:8000/redoc`

## 📁 Project Structure

```
ai-resume-analyzer/
├── 🐍 main.py              # FastAPI application entry point
├── 🧮 algo.py              # AI scoring & recommendation algorithms
├── 🛠️ skill.py             # Skills database & job role mappings
├── 📄 temp.py              # Resume parsing & text extraction
├── 📂 temp/                # Temporary file storage
├── 📋 requirements.txt     # Python dependencies
└── 📖 README.md            # Project documentation
```

## 🎯 Supported Job Roles

Our AI analyzes compatibility with 20+ job roles including:

- 🐍 **Python Developer** - 🔍 **Data Scientist** - ☁️ **Cloud Developer**
- 📊 **Data Analyst** - 💻 **Software Development Engineer** - 📈 **Sales Development Rep**
- 🔧 **Data Engineer** - 💼 **Business Analyst** - 🎨 **Front-End Developer**
- ⚙️ **Back-End Developer** - 🌐 **Full-Stack Developer** - 📱 **Mobile App Developer**
- 🚀 **DevOps Engineer** - 🤖 **ML Engineer** - 🔒 **Cybersecurity Specialist**
- 🎨 **UI/UX Designer** - 📋 **Product Manager** - 📢 **Marketing Specialist**
- 👥 **HR Specialist** - 📊 **Project Manager** - 🧪 **QA Engineer**

## 📊 API Usage Example

```python
import requests

# Analyze resume
with open('resume.pdf', 'rb') as file:
    response = requests.post(
        'http://localhost:8000/process-resume/',
        files={'file': file}
    )
    
result = response.json()
print(f"🎯 Resume Score: {result['Resume Score']}/100")
print(f"💼 Best Fit: {result['Recommendations']['Best Fit Job Roles'][0]['Job Role']}")
print(f"📊 Match: {result['Recommendations']['Best Fit Job Roles'][0]['Match Percentage']}")
```

## 🎪 Key Features Deep Dive

### 🧠 AI Scoring Algorithm
- **Smart Experience Weighting**: Evaluates years and relevance of experience
- **Skills Intelligence**: Matches against industry-standard skill requirements
- **Academic Excellence Bonus**: Enhanced scoring for high academic performers
- **Soft Skills Recognition**: Identifies leadership and teamwork capabilities

### 📚 Course Recommendations
Integrated with popular learning platforms:
- 🎓 Udemy - 🏛️ Coursera - 💼 LinkedIn Learning - 📺 YouTube

### 🔍 Advanced NLP Capabilities
- **Personal Info Extraction**: Name, contact, email detection
- **Skills Recognition**: 200+ technical and soft skills identification
- **Education Mining**: Degree, university, GPA, graduation year
- **Experience Analysis**: Job titles, dates, duration calculation

## 🤝 Contributing

We welcome contributions! 🎉

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

### 📝 Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Update skill sets in `skill.py` for new technologies
- Test with diverse resume formats

## ⚙️ Configuration

### 🔧 Environment Variables
```bash
TEMP_DIR=temp/  # Temporary file storage directory
```

### 🎛️ Customization Options
- **🛠️ Add New Skills**: Update `skills` tuple in `skill.py`
- **💼 Add Job Roles**: Extend `skill_set` dictionary with new roles
- **📊 Modify Scoring**: Adjust weights in `score_resume()` function

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨💻 Author

Created with ❤️ by [Jayesh Goel](https://github.com/jayesh-goel)

## 🙏 Acknowledgments

- 🌟 spaCy team for incredible NLP tools
- ⚡ FastAPI creators for the lightning-fast framework
- 📄 pdfminer contributors for PDF processing capabilities
- 🤝 All contributors and the open-source community

***

⭐ **Star this repository if it helped you!** ⭐

### 📸 Sample Output

```json
{
  "Resume Score": 87,
  "Recommendations": {
    "Best Fit Job Roles": [
      {
        "Job Role": "Python Developer",
        "Match Percentage": "85.50%",
        "Missing Skills": ["Docker", "Kubernetes"]
      }
    ],
    "Missing Skills to Improve": ["Docker", "Kubernetes", "AWS"],
    "Recommended Courses": [
      {
        "skill": "Docker",
        "courses": {
          "Udemy": "Docker courses",
          "Coursera": "Container technologies",
          "YouTube": "Docker tutorials"
        }
      }
    ]
  }
}
```

💡 **Pro Tip**: Use this tool to optimize your resume for specific job roles and identify skill gaps in your career development journey!

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/86258611/062d5494-f5fc-4e30-a93d-91544ada86d3/README.md
