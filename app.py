import streamlit as st
import pandas as pd
import plotly.express as px
import io

from modules.extract_text import extract_text
from modules.skills_extractor import extract_skills
from modules.scorer import calculate_score
from modules.matcher import calculate_semantic_similarity


# ==================================
# PAGE SETTINGS
# ==================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


# ==================================
# TITLE
# ==================================

st.title("📄 AI Resume Screening System")

st.write("Upload Resume and Job Description")


# ==================================
# RESUME UPLOAD
# ==================================

resumes = st.file_uploader(
    "Upload Resume(s) (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


# ==================================
# JOB DESCRIPTION UPLOAD
# ==================================

job = st.file_uploader(
    "Upload Job Description",
    type=["txt", "pdf", "docx"]
)


# ==================================
# ANALYZE BUTTON
# ==================================

if st.button("Analyze Resume"):

    if len(resumes) == 0 or job is None:

        st.warning(
            "Please upload both Resume and Job Description."
        )

    else:

        # ==================================
        # EXTRACT JOB DESCRIPTION
        # ==================================

        job_text = extract_text(job)

        job_skills = extract_skills(job_text)

        st.subheader("📋 Job Description")

        st.text_area(
            "Extracted Job Description",
            job_text,
            height=250
        )

        st.subheader("🎯 Required Skills")

        st.write(job_skills)


        # ==================================
        # STORE RESULTS
        # ==================================

        results = []


        # ==================================
        # ANALYZE EACH RESUME
        # ==================================

        for resume in resumes:

            # Extract Resume Text
            resume_text = extract_text(resume)

            # Extract Resume Skills
            resume_skills = extract_skills(resume_text)


            # ==================================
            # SKILL MATCH SCORE
            # ==================================

            score, matched, missing = calculate_score(
                resume_skills,
                job_skills
            )


            # ==================================
            # AI SEMANTIC SCORE
            # ==================================

            semantic_score = calculate_semantic_similarity(
                resume_text,
                job_text
            )


            # ==================================
            # FINAL AI SCORE
            # 60% Skill Match + 40% Semantic Match
            # ==================================

            final_score = round(
                (score * 0.60) +
                (semantic_score * 0.40),
                2
            )


            # ==================================
            # RESUME DETAILS
            # ==================================

            st.divider()

            st.subheader(
                f"📄 {resume.name}"
            )


            # Extracted Resume Text
            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=250,
                key=f"text_{resume.name}"
            )


            # Resume Skills
            st.write("### 🛠️ Resume Skills")
            st.write(resume_skills)


            # Matched Skills
            st.write("### ✅ Matched Skills")
            st.write(matched)


            # Missing Skills
            st.write("### ❌ Missing Skills")
            st.write(missing)


            # Skill Match Score
            st.metric(
                "Resume Match Score",
                f"{score}%"
            )


            # AI Semantic Score
            st.metric(
                "🤖 AI Semantic Match",
                f"{semantic_score}%"
            )


            # Final AI Score
            st.metric(
                "🏆 Final AI Score",
                f"{final_score}%"
            )


            # ==================================
            # SAVE RESULT
            # ==================================

            results.append({
                "Candidate": resume.name,
                "Skill Match Score": score,
                "AI Semantic Score": semantic_score,
                "Final AI Score": final_score,
                "Matched Skills": ", ".join(matched),
                "Missing Skills": ", ".join(missing)
            })


        # ==================================
        # CREATE DATAFRAME
        # ==================================

        df = pd.DataFrame(results)


        # ==================================
        # FINAL CANDIDATE RANKING
        # ==================================

        df = df.sort_values(
            by="Final AI Score",
            ascending=False
        )


        # ==================================
        # CANDIDATE RANKING
        # ==================================

        st.divider()

        st.subheader(
            "🏆 Candidate Ranking"
        )


        st.dataframe(
            df,
            use_container_width=True
        )


        # ==================================
        # AI SCORE DASHBOARD
        # ==================================

        st.divider()

        st.header(
            "📊 AI Score Dashboard"
        )


        # ==================================
        # DASHBOARD METRICS
        # ==================================

        total_candidates = len(df)


        average_score = round(
            df["Final AI Score"].mean(),
            2
        )


        highest_score = df["Final AI Score"].max()


        lowest_score = df["Final AI Score"].min()


        top_candidate = df.iloc[0]["Candidate"]


        # ==================================
        # METRICS ROW
        # ==================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "👥 Total Candidates",
                total_candidates
            )


        with col2:

            st.metric(
                "📊 Average Final Score",
                f"{average_score}%"
            )


        with col3:

            st.metric(
                "🏆 Highest Final Score",
                f"{highest_score}%"
            )


        with col4:

            st.metric(
                "📉 Lowest Final Score",
                f"{lowest_score}%"
            )


        # ==================================
        # TOP CANDIDATE
        # ==================================

        st.success(
            f"🏆 Top Candidate: {top_candidate} — {highest_score}%"
        )


        # ==================================
        # SCORE CHART
        # ==================================

        st.subheader(
            "📈 Candidate Final AI Score Comparison"
        )


        fig = px.bar(
            df,
            x="Candidate",
            y="Final AI Score",
            title="Final AI Resume Matching Scores"
        )


        fig.update_yaxes(
            range=[0, 100],
            title="Final AI Score (%)"
        )


        fig.update_xaxes(
            title="Candidates"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ==================================
        # EXPORT RESULTS
        # ==================================

        st.divider()

        st.header(
            "📥 Export Results"
        )


        # ==================================
        # CSV EXPORT
        # ==================================

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )


        # ==================================
        # EXCEL EXPORT
        # ==================================

        excel_buffer = io.BytesIO()


        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Resume Results"
            )


        excel_data = excel_buffer.getvalue()


        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name="resume_screening_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

