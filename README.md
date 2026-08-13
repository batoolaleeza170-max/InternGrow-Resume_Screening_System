# 📄 Intelligent Resume Screening System

An AI-powered Resume Screening System built with Python and Streamlit that automatically analyzes resumes and compares them with job descriptions.

The system extracts resume text, identifies skills, calculates skill-match scores, performs AI-based semantic matching, ranks candidates, and allows HR/recruiters to export screening results.

---

## 🚀 Features

- 📄 Upload multiple resumes
- 📑 Support PDF and DOCX resumes
- 📝 Upload Job Description
- 🔍 Automatic text extraction
- 🛠️ NLP-based skill extraction
- 🎯 Required skill identification
- ✅ Matched skills detection
- ❌ Missing skills detection
- 📊 Resume Skill Match Score
- 🤖 AI Semantic Matching
- 🏆 Final AI Score
- 🥇 Automatic Candidate Ranking
- 📈 AI Score Dashboard
- 📄 CSV Export
- 📊 Excel Export

---

## 🧠 AI Scoring

The system calculates the final candidate score using two factors:

### Skill Match Score
Measures how many required job skills are present in the candidate's resume.

### AI Semantic Score
Compares the overall meaning and relevance of the resume with the job description.

### Final AI Score

```text
Final AI Score =
(Skill Match Score × 60%)
+
(AI Semantic Score × 40%)
