import streamlit as st

# ============================================================
# SKILL-TO-JOB MATCHER
# Complete Mini Project - Python + Streamlit
# ============================================================

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Skill-to-Job Matcher",
    page_icon="💼",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.job-title {
    font-size: 25px;
    font-weight: bold;
}

.match-score {
    font-size: 20px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# JOB DATA
# ============================================================

jobs = {

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "TensorFlow"
    ],

    "Python Developer": [
        "Python",
        "Django",
        "SQL",
        "Git"
    ],

    "Java Developer": [
        "Java",
        "SQL",
        "Git",
        "Spring Boot"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "TensorFlow"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Python",
        "SQL",
        "Git"
    ]
}


# ============================================================
# ALL AVAILABLE SKILLS
# ============================================================

all_skills = sorted(set(
    skill
    for job_skills in jobs.values()
    for skill in job_skills
))


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💼 Skill-to-Job Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Find the right job based on your skills'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# USER INFORMATION
# ============================================================

st.header("👤 Candidate Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Enter Your Name",
        placeholder="Example: Harmain Banu"
    )

with col2:

    email = st.text_input(
        "Enter Your Email",
        placeholder="Example: example@gmail.com"
    )


# ============================================================
# PREFERRED JOB
# ============================================================

preferred_job = st.selectbox(
    "🎯 Select Your Preferred Job Role",
    ["No Preference"] + list(jobs.keys())
)


# ============================================================
# SKILL SELECTION
# ============================================================

st.header("🛠️ Your Skills")

selected_skills = st.multiselect(
    "Select the skills you currently have:",
    all_skills,
    placeholder="Choose your skills"
)


# ============================================================
# CUSTOM SKILLS
# ============================================================

st.write("### ➕ Add Other Skills")

custom_skills = st.text_input(
    "Enter additional skills separated by commas",
    placeholder="Example: AWS, Docker, C++, Linux"
)

if custom_skills:

    extra_skills = [
        skill.strip()
        for skill in custom_skills.split(",")
        if skill.strip()
    ]

    selected_skills = selected_skills + extra_skills


# ============================================================
# FIND MATCH BUTTON
# ============================================================

st.divider()

find_button = st.button(
    "🔍 FIND MY JOB MATCHES",
    use_container_width=True
)


# ============================================================
# JOB MATCHING
# ============================================================

if find_button:

    # ---------------- VALIDATION ----------------

    if not name:

        st.error("❌ Please enter your name.")

    elif not selected_skills:

        st.error("❌ Please select at least one skill.")

    else:

        # Convert user skills to lowercase
        user_skills = [
            skill.lower().strip()
            for skill in selected_skills
        ]

        results = []


        # ====================================================
        # COMPARE USER SKILLS WITH JOB SKILLS
        # ====================================================

        for job_name, required_skills in jobs.items():

            matching_skills = []

            missing_skills = []


            for skill in required_skills:

                if skill.lower() in user_skills:

                    matching_skills.append(skill)

                else:

                    missing_skills.append(skill)


            # Calculate percentage

            match_percentage = round(
                (
                    len(matching_skills)
                    /
                    len(required_skills)
                ) * 100
            )


            results.append({

                "job": job_name,

                "score": match_percentage,

                "matching": matching_skills,

                "missing": missing_skills

            })


        # ====================================================
        # SORT BY HIGHEST MATCH
        # ====================================================

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        # ====================================================
        # PREFERRED JOB HANDLING
        # ====================================================

        if preferred_job != "No Preference":

            preferred_result = None

            other_results = []

            for result in results:

                if result["job"] == preferred_job:

                    preferred_result = result

                else:

                    other_results.append(result)


            if preferred_result:

                results = [
                    preferred_result
                ] + other_results


        # ====================================================
        # DISPLAY USER INFORMATION
        # ====================================================

        st.divider()

        st.success(
            f"Welcome {name}! 🎉"
        )

        if email:

            st.write(
                f"📧 Email: **{email}**"
            )


        # ====================================================
        # BEST MATCH
        # ====================================================

        best_job = results[0]


        st.header("🏆 Best Job Match")


        st.markdown(
            f"""
            <div class="card">

            <div class="job-title">
            {best_job["job"]}
            </div>

            <div class="match-score">
            Match Score: {best_job["score"]}%
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.progress(
            best_job["score"] / 100
        )


        # ====================================================
        # JOB RECOMMENDATIONS
        # ====================================================

        st.header("📊 Job Recommendations")


        for index, result in enumerate(results, 1):

            st.markdown(
                f"""
                <div class="card">

                <div class="job-title">
                {index}. {result["job"]}
                </div>

                <div class="match-score">
                Match: {result["score"]}%
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.progress(
                result["score"] / 100
            )


            col1, col2 = st.columns(2)


            # ---------------- MATCHING SKILLS ----------------

            with col1:

                st.subheader("✅ Matching Skills")

                if result["matching"]:

                    for skill in result["matching"]:

                        st.write(
                            f"✔️ {skill}"
                        )

                else:

                    st.write(
                        "No matching skills"
                    )


            # ---------------- MISSING SKILLS ----------------

            with col2:

                st.subheader("📚 Missing Skills")

                if result["missing"]:

                    for skill in result["missing"]:

                        st.write(
                            f"❌ {skill}"
                        )

                else:

                    st.success(
                        "You have all required skills!"
                    )


            st.divider()


        # ====================================================
        # LEARNING RECOMMENDATION
        # ====================================================

        st.header("📖 Recommended Learning")


        if best_job["missing"]:

            st.write(
                f"To improve your chances of becoming a "
                f"**{best_job['job']}**, you should learn:"
            )


            for skill in best_job["missing"]:

                st.info(
                    f"📘 Learn {skill}"
                )


        else:

            st.success(
                "🎉 Excellent! You already have all "
                "the required skills for your best match."
            )


        # ====================================================
        # CAREER MESSAGE
        # ====================================================

        st.header("💡 Career Advice")


        if best_job["score"] >= 80:

            st.success(
                "You are highly suitable for this job role. "
                "Focus on projects, internships and interview preparation."
            )

        elif best_job["score"] >= 50:

            st.warning(
                "You have a good foundation. "
                "Learn the missing skills and build practical projects."
            )

        else:

            st.info(
                "You need to develop more relevant skills. "
                "Start with the missing skills and practice through projects."
            )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💼 About Project")

st.sidebar.write(
    """
    Skill-to-Job Matcher is an intelligent career
    recommendation mini project.

    It compares the user's skills with the skills
    required for different job roles and recommends
    suitable career opportunities.
    """
)


st.sidebar.subheader("Features")

st.sidebar.write("✅ Skill Matching")
st.sidebar.write("✅ Job Recommendation")
st.sidebar.write("✅ Match Percentage")
st.sidebar.write("✅ Missing Skill Analysis")
st.sidebar.write("✅ Learning Recommendation")
st.sidebar.write("✅ Career Advice")


st.sidebar.subheader("Technology")

st.sidebar.write("🐍 Python")
st.sidebar.write("🎨 Streamlit")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Skill-to-Job Matcher | Python + Streamlit Mini Project"
)