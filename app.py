
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Skill-to-Job Matcher",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# CUSTOM CSS - LIGHT BACKGROUND AND READABLE TEXT
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
    color: #1f2937;
}

.stApp h1, .stApp h2, .stApp h3,
.stApp p, .stApp label, .stApp li {
    color: #1f2937;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #1d4ed8;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #475569;
    margin-bottom: 25px;
}

.card {
    background-color: #ffffff;
    color: #1f2937;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dbe3ef;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    margin-bottom: 12px;
}

.job-title {
    font-size: 24px;
    font-weight: bold;
    color: #1d4ed8;
}

.match-score {
    font-size: 20px;
    font-weight: bold;
    color: #15803d;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

div.stButton > button p {
    color: white !important;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #eaf0fa;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# JOB ROLES AND REQUIRED SKILLS
# =========================================================
jobs = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Tableau"
    ],
    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy",
        "Machine Learning", "TensorFlow"
    ],
    "Python Developer": [
        "Python", "Django", "SQL", "Git"
    ],
    "Java Developer": [
        "Java", "SQL", "Git", "Spring Boot"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Git"
    ],
    "Machine Learning Engineer": [
        "Python", "Pandas", "NumPy",
        "Machine Learning", "TensorFlow"
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Python", "SQL", "Git"
    ]
}

all_skills = sorted({
    skill
    for skill_list in jobs.values()
    for skill in skill_list
})

# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="title">💼 Skill-to-Job Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Find suitable job roles based on your skills'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# CANDIDATE INFORMATION
# =========================================================
st.header("👤 Candidate Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Enter Your Name",
        placeholder="Example: Harmain Banu"
    )

with col2:
    email = st.text_input(
        "Enter Your Email (optional)",
        placeholder="Example: example@gmail.com"
    )

# =========================================================
# JOB PREFERENCE
# =========================================================
st.header("🎯 Job Preference")

preferred_job = st.selectbox(
    "Select your preferred job role",
    ["No Preference"] + list(jobs.keys())
)

# =========================================================
# SKILL SELECTION
# =========================================================
st.header("🛠️ Your Skills")

selected_skills = st.multiselect(
    "Select the skills you currently have",
    options=all_skills,
    placeholder="Choose one or more skills"
)

custom_skills = st.text_input(
    "Add other skills (separate them with commas)",
    placeholder="Example: AWS, Docker, Linux"
)

if custom_skills.strip():
    extra_skills = [
        skill.strip()
        for skill in custom_skills.split(",")
        if skill.strip()
    ]
    selected_skills = selected_skills + extra_skills

st.caption(
    "Tip: Select all the skills you know to get a more accurate match."
)

st.divider()

# =========================================================
# FIND JOB MATCHES
# =========================================================
find_button = st.button(
    "🔍 FIND MY JOB MATCHES",
    use_container_width=True
)

if find_button:

    if not name.strip():
        st.error("Please enter your name.")

    elif not selected_skills:
        st.error("Please select at least one skill.")

    else:
        # Make matching case-insensitive.
        user_skills = {
            skill.strip().casefold()
            for skill in selected_skills
            if skill.strip()
        }

        # Select one job or compare all jobs.
        if preferred_job == "No Preference":
            jobs_to_check = jobs.items()
        else:
            jobs_to_check = [
                (preferred_job, jobs[preferred_job])
            ]

        results = []

        for job_name, required_skills in jobs_to_check:
            matching_skills = [
                skill for skill in required_skills
                if skill.casefold() in user_skills
            ]

            missing_skills = [
                skill for skill in required_skills
                if skill.casefold() not in user_skills
            ]

            score = round(
                len(matching_skills) / len(required_skills) * 100
            )

            results.append({
                "job": job_name,
                "score": score,
                "matching": matching_skills,
                "missing": missing_skills,
                "required": required_skills
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # =================================================
        # CANDIDATE SUMMARY
        # =================================================
        st.divider()
        st.success(f"Welcome, {name.strip()}! 🎉")

        if email.strip():
            st.write(f"📧 Email: {email.strip()}")

        # =================================================
        # BEST JOB MATCH
        # =================================================
        best_job = results[0]

        st.header("🏆 Best Job Match")

        st.markdown(
            f"""
            <div class="card">
                <div class="job-title">{best_job["job"]}</div>
                <div class="match-score">
                    Match Score: {best_job["score"]}%
                </div>
                <p>Matching skills: {len(best_job["matching"])}
                out of {len(best_job["required"])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(best_job["score"] / 100)

        # =================================================
        # JOB RECOMMENDATIONS
        # =================================================
        st.header("📊 Job Recommendations")

        if preferred_job != "No Preference":
            st.caption(
                f"Showing results only for your selected role: "
                f"{preferred_job}."
            )
        else:
            st.caption(
                "All job roles are ranked from highest to lowest match."
            )

        for index, result in enumerate(results, start=1):

            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="job-title">
                        {index}. {result["job"]}
                    </div>
                    <div class="match-score">
                        Match: {result["score"]}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.progress(result["score"] / 100)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("✅ Matching Skills")

                    if result["matching"]:
                        for skill in result["matching"]:
                            st.write(f"✔️ {skill}")
                    else:
                        st.write("No matching skills yet.")

                with col2:
                    st.subheader("📚 Missing Skills")

                    if result["missing"]:
                        for skill in result["missing"]:
                            st.write(f"❌ {skill}")
                    else:
                        st.success("You have all required skills!")

        # =================================================
        # RECOMMENDED LEARNING
        # =================================================
        st.divider()
        st.header("📖 Recommended Learning")

        if best_job["missing"]:
            st.write(
                f"To improve your match for **{best_job['job']}**, "
                "focus on learning these skills:"
            )

            for skill in best_job["missing"]:
                st.info(f"📘 Learn {skill}")

        else:
            st.success(
                "🎉 You have all the listed skills for this job role!"
            )

        # =================================================
        # CAREER ADVICE
        # =================================================
        st.header("💡 Career Advice")

        if best_job["score"] >= 80:
            st.success(
                "You have a strong skill match. Build projects, "
                "gain practical experience, and prepare for interviews."
            )

        elif best_job["score"] >= 50:
            st.warning(
                "You have a reasonable foundation. Learn the missing "
                "skills and practise with small projects."
            )

        else:
            st.info(
                "Start with the missing skills, practise regularly, "
                "and build projects to strengthen your profile."
            )

        st.caption(
            "Match percentages are calculated from the predefined "
            "skills for each job role. They do not guarantee employment."
        )

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("💼 About This Project")

st.sidebar.write(
    "Skill-to-Job Matcher compares your selected skills with "
    "predefined job requirements and identifies possible skill gaps."
)

st.sidebar.subheader("Features")
st.sidebar.write("✅ Skill Matching")
st.sidebar.write("✅ Job Recommendations")
st.sidebar.write("✅ Match Percentage")
st.sidebar.write("✅ Missing Skill Analysis")
st.sidebar.write("✅ Recommended Learning")
st.sidebar.write("✅ Career Advice")

st.sidebar.subheader("Technologies")
st.sidebar.write("🐍 Python")
st.sidebar.write("🎨 Streamlit")

st.sidebar.divider()
st.sidebar.caption("Skill-to-Job Matcher | Mini Project")

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption(
    "Skill-to-Job Matcher | Built with Python and Streamlit"
)
