
import streamlit as st
import re

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Skill-to-Job Matcher",
    page_icon="💼",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #ffffff;
}

h1, h2, h3, h4, p, label, li {
    color: #ffffff !important;
}

.main-title {
    text-align: center;
    color: #ffffff !important;
    font-size: 38px;
    font-weight: bold;
    padding: 10px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1 !important;
    font-size: 17px;
    margin-bottom: 25px;
}

.dataset-summary-card {
    background-color: #1e293b;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #475569;
    margin: 15px 0 25px 0;
}

.dataset-summary-title {
    color: #ffffff !important;
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 15px;
}

.dataset-summary-text {
    color: #ffffff !important;
    font-size: 16px;
    line-height: 2;
}

.result-card {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #475569;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #475569;
}

div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 9px 18px;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

div[data-testid="stProgress"] {
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# JOB ROLE DATASET
# --------------------------------------------------
JOB_ROLES = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Tableau", "Statistics", "Data Visualization"
    ],

    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy",
        "Machine Learning", "Statistics", "Scikit-learn"
    ],

    "Python Developer": [
        "Python", "Django", "SQL", "Git",
        "REST API", "Problem Solving", "Data Structures"
    ],

    "Java Developer": [
        "Java", "SQL", "Spring Boot", "Git",
        "REST API", "Problem Solving", "Data Structures"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Git", "REST API"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Pandas",
        "NumPy", "TensorFlow", "Scikit-learn", "Statistics"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Python", "SQL", "Git", "REST API"
    ],

    "Cloud Engineer": [
        "AWS", "Linux", "Networking", "Docker",
        "Kubernetes", "Python", "Security"
    ],

    "DevOps Engineer": [
        "Linux", "Git", "Docker", "Kubernetes",
        "Jenkins", "AWS", "CI/CD", "Ansible"
    ],

    "Cybersecurity Analyst": [
        "Networking", "Linux", "Cybersecurity",
        "Ethical Hacking", "Security Tools", "Python"
    ],

    "Data Engineer": [
        "Python", "SQL", "Apache Spark", "Airflow",
        "ETL", "Data Warehousing", "AWS"
    ],

    "Business Analyst": [
        "Excel", "SQL", "Power BI",
        "Communication", "Requirements Analysis",
        "Data Visualization"
    ],

    "UI/UX Designer": [
        "Figma", "Wireframing", "Prototyping",
        "UI Design", "UX Research", "Communication"
    ],

    "Mobile App Developer": [
        "Flutter", "Dart", "Firebase",
        "REST API", "Git", "UI Design"
    ],

    "Software Tester": [
        "Manual Testing", "Selenium", "Postman",
        "Test Cases", "SQL", "Java", "Python"
    ],

    "Database Administrator": [
        "SQL", "MySQL", "PostgreSQL",
        "Database Design", "Backup and Recovery",
        "Database Security", "Linux"
    ],

    "Android Developer": [
        "Kotlin", "Java", "Android Studio",
        "Firebase", "REST API", "Git"
    ],

    "Node.js Developer": [
        "JavaScript", "Node.js", "Express.js",
        "MongoDB", "REST API", "Git"
    ],

    "PHP Developer": [
        "PHP", "Laravel", "MySQL",
        "HTML", "CSS", "JavaScript", "REST API"
    ],

    "Data Visualization Specialist": [
        "Power BI", "Tableau", "Excel",
        "SQL", "Python", "Data Visualization", "Statistics"
    ]
}

# --------------------------------------------------
# EXPANDED SKILL DATASET
# --------------------------------------------------
ALL_SKILLS = sorted({
    skill
    for skills in JOB_ROLES.values()
    for skill in skills
})

# --------------------------------------------------
# LEARNING RESOURCES
# Links include tutorials, documentation, courses,
# video searches and certification information.
# --------------------------------------------------
RESOURCES = {
    "Python": [
        ("Website", "Python Official Tutorial",
         "https://docs.python.org/3/tutorial/"),
        ("Videos", "Python Tutorials",
         "https://www.youtube.com/results?search_query=Python+full+course"),
        ("Course", "Python Courses",
         "https://www.coursera.org/search?query=python"),
        ("Certification", "Python Certification Options",
         "https://www.coursera.org/search?query=python+certificate")
    ],

    "SQL": [
        ("Website", "SQLBolt Interactive Lessons",
         "https://sqlbolt.com/"),
        ("Videos", "SQL Tutorial Videos",
         "https://www.youtube.com/results?search_query=SQL+full+course"),
        ("Course", "SQL Courses",
         "https://www.coursera.org/search?query=SQL")
    ],

    "Excel": [
        ("Website", "Microsoft Excel Help",
         "https://support.microsoft.com/excel"),
        ("Videos", "Excel Tutorials",
         "https://www.youtube.com/results?search_query=Excel+full+course"),
        ("Course", "Excel Courses",
         "https://www.coursera.org/search?query=Excel")
    ],

    "Power BI": [
        ("Website", "Microsoft Power BI Learning",
         "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"),
        ("Videos", "Power BI Tutorials",
         "https://www.youtube.com/results?search_query=Power+BI+full+course"),
        ("Certification", "Microsoft PL-300",
         "https://learn.microsoft.com/en-us/credentials/certifications/power-bi-data-analyst-associate/")
    ],

    "Tableau": [
        ("Website", "Tableau Learning",
         "https://www.tableau.com/learn"),
        ("Videos", "Tableau Tutorials",
         "https://www.youtube.com/results?search_query=Tableau+full+course"),
        ("Course", "Tableau Courses",
         "https://www.coursera.org/search?query=Tableau")
    ],

    "Pandas": [
        ("Website", "Pandas Documentation",
         "https://pandas.pydata.org/docs/getting_started/"),
        ("Videos", "Pandas Tutorials",
         "https://www.youtube.com/results?search_query=Python+Pandas+tutorial"),
        ("Course", "Pandas Courses",
         "https://www.kaggle.com/learn/pandas")
    ],

    "NumPy": [
        ("Website", "NumPy Learning",
         "https://numpy.org/learn/"),
        ("Videos", "NumPy Tutorials",
         "https://www.youtube.com/results?search_query=NumPy+tutorial"),
        ("Course", "NumPy Courses",
         "https://www.coursera.org/search?query=NumPy")
    ],

    "Machine Learning": [
        ("Website", "Google Machine Learning Crash Course",
         "https://developers.google.com/machine-learning/crash-course"),
        ("Videos", "Machine Learning Tutorials",
         "https://www.youtube.com/results?search_query=Machine+Learning+full+course"),
        ("Course", "Machine Learning Courses",
         "https://www.coursera.org/search?query=machine+learning")
    ],

    "TensorFlow": [
        ("Website", "TensorFlow Tutorials",
         "https://www.tensorflow.org/tutorials"),
        ("Videos", "TensorFlow Tutorials",
         "https://www.youtube.com/results?search_query=TensorFlow+full+course"),
        ("Course", "TensorFlow Courses",
         "https://www.coursera.org/search?query=TensorFlow")
    ],

    "Scikit-learn": [
        ("Website", "Scikit-learn User Guide",
         "https://scikit-learn.org/stable/user_guide.html"),
        ("Videos", "Scikit-learn Tutorials",
         "https://www.youtube.com/results?search_query=scikit-learn+tutorial")
    ],

    "Statistics": [
        ("Website", "Khan Academy Statistics",
         "https://www.khanacademy.org/math/statistics-probability"),
        ("Videos", "Statistics Tutorials",
         "https://www.youtube.com/results?search_query=statistics+for+data+science"),
        ("Course", "Statistics Courses",
         "https://www.coursera.org/search?query=statistics")
    ],

    "Django": [
        ("Website", "Django Official Tutorial",
         "https://docs.djangoproject.com/en/stable/intro/tutorial01/"),
        ("Videos", "Django Tutorials",
         "https://www.youtube.com/results?search_query=Django+full+course"),
        ("Course", "Django Courses",
         "https://www.coursera.org/search?query=Django")
    ],

    "Java": [
        ("Website", "Dev.java Learning",
         "https://dev.java/learn/"),
        ("Videos", "Java Full Course",
         "https://www.youtube.com/results?search_query=Java+full+course"),
        ("Course", "Java Courses",
         "https://www.coursera.org/search?query=Java")
    ],

    "Spring Boot": [
        ("Website", "Spring Guides",
         "https://spring.io/guides"),
        ("Videos", "Spring Boot Tutorials",
         "https://www.youtube.com/results?search_query=Spring+Boot+full+course"),
        ("Course", "Spring Boot Courses",
         "https://www.udemy.com/courses/search/?q=spring%20boot")
    ],

    "HTML": [
        ("Website", "MDN HTML Guide",
         "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content"),
        ("Videos", "HTML Tutorials",
         "https://www.youtube.com/results?search_query=HTML+full+course")
    ],

    "CSS": [
        ("Website", "MDN CSS Guide",
         "https://developer.mozilla.org/en-US/docs/Web/CSS"),
        ("Videos", "CSS Tutorials",
         "https://www.youtube.com/results?search_query=CSS+full+course")
    ],

    "JavaScript": [
        ("Website", "JavaScript Guide",
         "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
        ("Videos", "JavaScript Full Course",
         "https://www.youtube.com/results?search_query=JavaScript+full+course"),
        ("Course", "JavaScript Courses",
         "https://www.freecodecamp.org/learn/")
    ],

    "React": [
        ("Website", "React Official Learn Guide",
         "https://react.dev/learn"),
        ("Videos", "React Tutorials",
         "https://www.youtube.com/results?search_query=React+full+course"),
        ("Course", "React Courses",
         "https://www.coursera.org/search?query=React")
    ],

    "Git": [
        ("Website", "Git Official Book",
         "https://git-scm.com/book/en/v2"),
        ("Videos", "Git and GitHub Tutorials",
         "https://www.youtube.com/results?search_query=Git+and+GitHub+full+course"),
        ("Course", "Git Courses",
         "https://www.coursera.org/search?query=Git")
    ],

    "REST API": [
        ("Website", "MDN HTTP Guide",
         "https://developer.mozilla.org/en-US/docs/Web/HTTP"),
        ("Videos", "REST API Tutorials",
         "https://www.youtube.com/results?search_query=REST+API+tutorial"),
        ("Course", "API Courses",
         "https://www.coursera.org/search?query=REST+API")
    ],

    "Problem Solving": [
        ("Website", "HackerRank Practice",
         "https://www.hackerrank.com/"),
        ("Videos", "Problem Solving Tutorials",
         "https://www.youtube.com/results?search_query=programming+problem+solving"),
        ("Practice", "LeetCode",
         "https://leetcode.com/")
    ],

    "Data Structures": [
        ("Website", "GeeksforGeeks DSA",
         "https://www.geeksforgeeks.org/data-structures/"),
        ("Videos", "DSA Full Course",
         "https://www.youtube.com/results?search_query=data+structures+algorithms+full+course"),
        ("Practice", "LeetCode",
         "https://leetcode.com/")
    ],

    "AWS": [
        ("Website", "AWS Skill Builder",
         "https://skillbuilder.aws/"),
        ("Videos", "AWS Tutorials",
         "https://www.youtube.com/results?search_query=AWS+cloud+practitioner+course"),
        ("Certification", "AWS Certifications",
         "https://aws.amazon.com/certification/")
    ],

    "Linux": [
        ("Website", "Linux Journey",
         "https://linuxjourney.com/"),
        ("Videos", "Linux Tutorials",
         "https://www.youtube.com/results?search_query=Linux+full+course")
    ],

    "Networking": [
        ("Website", "Cisco Networking Academy",
         "https://www.netacad.com/"),
        ("Videos", "Computer Networking Tutorials",
         "https://www.youtube.com/results?search_query=computer+networking+full+course"),
        ("Certification", "Cisco Certifications",
         "https://www.cisco.com/site/us/en/learn/training-certifications/certifications/index.html")
    ],

    "Docker": [
        ("Website", "Docker Get Started",
         "https://docs.docker.com/get-started/"),
        ("Videos", "Docker Tutorials",
         "https://www.youtube.com/results?search_query=Docker+full+course")
    ],

    "Kubernetes": [
        ("Website", "Kubernetes Basics",
         "https://kubernetes.io/docs/tutorials/kubernetes-basics/"),
        ("Videos", "Kubernetes Tutorials",
         "https://www.youtube.com/results?search_query=Kubernetes+full+course")
    ],

    "Jenkins": [
        ("Website", "Jenkins User Documentation",
         "https://www.jenkins.io/doc/"),
        ("Videos", "Jenkins Tutorials",
         "https://www.youtube.com/results?search_query=Jenkins+CI+CD+tutorial")
    ],

    "Ansible": [
        ("Website", "Ansible Getting Started",
         "https://docs.ansible.com/ansible/latest/getting_started/"),
        ("Videos", "Ansible Tutorials",
         "https://www.youtube.com/results?search_query=Ansible+tutorial")
    ],

    "CI/CD": [
        ("Website", "GitHub Actions Documentation",
         "https://docs.github.com/en/actions"),
        ("Videos", "CI/CD Tutorials",
         "https://www.youtube.com/results?search_query=CI+CD+pipeline+tutorial")
    ],

    "Cybersecurity": [
        ("Website", "Cisco Skills for All",
         "https://skillsforall.com/"),
        ("Videos", "Cybersecurity Tutorials",
         "https://www.youtube.com/results?search_query=cybersecurity+full+course"),
        ("Certification", "CompTIA Security+",
         "https://www.comptia.org/certifications/security")
    ],

    "Ethical Hacking": [
        ("Website", "TryHackMe",
         "https://tryhackme.com/"),
        ("Videos", "Ethical Hacking Tutorials",
         "https://www.youtube.com/results?search_query=ethical+hacking+course"),
        ("Certification", "Certified Ethical Hacker",
         "https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/")
    ],

    "Security Tools": [
        ("Website", "OWASP Web Security",
         "https://owasp.org/"),
        ("Videos", "Cybersecurity Tools Tutorials",
         "https://www.youtube.com/results?search_query=cybersecurity+tools+tutorial")
    ],

    "Apache Spark": [
        ("Website", "Apache Spark Documentation",
         "https://spark.apache.org/docs/latest/"),
        ("Videos", "Apache Spark Tutorials",
         "https://www.youtube.com/results?search_query=Apache+Spark+tutorial")
    ],

    "Airflow": [
        ("Website", "Apache Airflow Documentation",
         "https://airflow.apache.org/docs/"),
        ("Videos", "Airflow Tutorials",
         "https://www.youtube.com/results?search_query=Apache+Airflow+tutorial")
    ],

    "ETL": [
        ("Website", "Microsoft Data Integration",
         "https://learn.microsoft.com/en-us/azure/data-factory/"),
        ("Videos", "ETL Tutorials",
         "https://www.youtube.com/results?search_query=ETL+data+engineering+tutorial")
    ],

    "Data Warehousing": [
        ("Website", "Google Cloud Data Warehouse",
         "https://cloud.google.com/learn/what-is-a-data-warehouse"),
        ("Videos", "Data Warehousing Tutorials",
         "https://www.youtube.com/results?search_query=data+warehousing+tutorial")
    ],

    "Data Visualization": [
        ("Website", "Data Visualization Resources",
         "https://www.tableau.com/learn/articles/data-visualization"),
        ("Videos", "Data Visualization Tutorials",
         "https://www.youtube.com/results?search_query=data+visualization+tutorial")
    ],

    "Communication": [
        ("Website", "British Council Learn English",
         "https://learnenglish.britishcouncil.org/"),
        ("Videos", "Communication Skills Tutorials",
         "https://www.youtube.com/results?search_query=communication+skills+course")
    ],

    "Requirements Analysis": [
        ("Website", "Atlassian Requirements Guide",
         "https://www.atlassian.com/agile/product-management/requirements"),
        ("Videos", "Business Analysis Tutorials",
         "https://www.youtube.com/results?search_query=requirements+analysis+tutorial")
    ],

    "Figma": [
        ("Website", "Figma Learn",
         "https://help.figma.com/"),
        ("Videos", "Figma Tutorials",
         "https://www.youtube.com/results?search_query=Figma+full+course")
    ],

    "Wireframing": [
        ("Website", "Figma Design Resources",
         "https://www.figma.com/resource-library/"),
        ("Videos", "Wireframing Tutorials",
         "https://www.youtube.com/results?search_query=wireframing+for+beginners")
    ],

    "Prototyping": [
        ("Website", "Figma Prototyping Guide",
         "https://help.figma.com/hc/en-us/categories/360002042553"),
        ("Videos", "Prototyping Tutorials",
         "https://www.youtube.com/results?search_query=Figma+prototyping+tutorial")
    ],

    "UI Design": [
        ("Website", "Material Design",
         "https://m3.material.io/"),
        ("Videos", "UI Design Tutorials",
         "https://www.youtube.com/results?search_query=UI+design+course")
    ],

    "UX Research": [
        ("Website", "Nielsen Norman Group",
         "https://www.nngroup.com/articles/"),
        ("Videos", "UX Research Tutorials",
         "https://www.youtube.com/results?search_query=UX+research+course")
    ],

    "Flutter": [
        ("Website", "Flutter Documentation",
         "https://docs.flutter.dev/"),
        ("Videos", "Flutter Full Course",
         "https://www.youtube.com/results?search_query=Flutter+full+course"),
        ("Course", "Flutter Courses",
         "https://www.coursera.org/search?query=Flutter")
    ],

    "Dart": [
        ("Website", "Dart Documentation",
         "https://dart.dev/guides"),
        ("Videos", "Dart Tutorials",
         "https://www.youtube.com/results?search_query=Dart+programming+tutorial")
    ],

    "Firebase": [
        ("Website", "Firebase Documentation",
         "https://firebase.google.com/docs"),
        ("Videos", "Firebase Tutorials",
         "https://www.youtube.com/results?search_query=Firebase+tutorial")
    ],

    "Kotlin": [
        ("Website", "Kotlin Documentation",
         "https://kotlinlang.org/docs/home.html"),
        ("Videos", "Kotlin Tutorials",
         "https://www.youtube.com/results?search_query=Kotlin+full+course")
    ],

    "Android Studio": [
        ("Website", "Android Developers",
         "https://developer.android.com/"),
        ("Videos", "Android Studio Tutorials",
         "https://www.youtube.com/results?search_query=Android+Studio+tutorial")
    ],

    "Manual Testing": [
        ("Website", "ISTQB",
         "https://www.istqb.org/"),
        ("Videos", "Manual Testing Tutorials",
         "https://www.youtube.com/results?search_query=software+manual+testing+course")
    ],

    "Selenium": [
        ("Website", "Selenium Documentation",
         "https://www.selenium.dev/documentation/"),
        ("Videos", "Selenium Tutorials",
         "https://www.youtube.com/results?search_query=Selenium+automation+testing+course")
    ],

    "Postman": [
        ("Website", "Postman Learning Center",
         "https://learning.postman.com/"),
        ("Videos", "Postman API Testing Tutorials",
         "https://www.youtube.com/results?search_query=Postman+API+testing+tutorial")
    ],

    "Test Cases": [
        ("Website", "Test Case Writing Guide",
         "https://www.browserstack.com/guide/test-case"),
        ("Videos", "Test Case Tutorials",
         "https://www.youtube.com/results?search_query=how+to+write+test+cases")
    ],

    "MySQL": [
        ("Website", "MySQL Documentation",
         "https://dev.mysql.com/doc/"),
        ("Videos", "MySQL Tutorials",
         "https://www.youtube.com/results?search_query=MySQL+full+course")
    ],

    "PostgreSQL": [
        ("Website", "PostgreSQL Tutorial",
         "https://www.postgresql.org/docs/current/tutorial.html"),
        ("Videos", "PostgreSQL Tutorials",
         "https://www.youtube.com/results?search_query=PostgreSQL+full+course")
    ],

    "Database Design": [
        ("Website", "Database Design Basics",
         "https://www.geeksforgeeks.org/database-design/"),
        ("Videos", "Database Design Tutorials",
         "https://www.youtube.com/results?search_query=database+design+tutorial")
    ],

    "Backup and Recovery": [
        ("Website", "MySQL Backup Documentation",
         "https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html"),
        ("Videos", "Database Backup Tutorials",
         "https://www.youtube.com/results?search_query=database+backup+recovery+tutorial")
    ],

    "Database Security": [
        ("Website", "OWASP Database Security",
         "https://owasp.org/"),
        ("Videos", "Database Security Tutorials",
         "https://www.youtube.com/results?search_query=database+security+tutorial")
    ],

    "Node.js": [
        ("Website", "Node.js Documentation",
         "https://nodejs.org/en/learn"),
        ("Videos", "Node.js Full Course",
         "https://www.youtube.com/results?search_query=Node.js+full+course"),
        ("Course", "Node.js Courses",
         "https://www.coursera.org/search?query=Node.js")
    ],

    "Express.js": [
        ("Website", "Express.js Guide",
         "https://expressjs.com/"),
        ("Videos", "Express.js Tutorials",
         "https://www.youtube.com/results?search_query=Express.js+tutorial")
    ],

    "MongoDB": [
        ("Website", "MongoDB University",
         "https://learn.mongodb.com/"),
        ("Videos", "MongoDB Tutorials",
         "https://www.youtube.com/results?search_query=MongoDB+full+course")
    ],

    "PHP": [
        ("Website", "PHP Official Manual",
         "https://www.php.net/manual/en/"),
        ("Videos", "PHP Full Course",
         "https://www.youtube.com/results?search_query=PHP+full+course")
    ],

    "Laravel": [
        ("Website", "Laravel Documentation",
         "https://laravel.com/docs"),
        ("Videos", "Laravel Tutorials",
         "https://www.youtube.com/results?search_query=Laravel+full+course")
    ]
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def normalize_skill(skill):
    return re.sub(r"\s+", " ", skill.strip().lower())


def calculate_match(user_skills, required_skills):
    user_set = {normalize_skill(s) for s in user_skills}
    required_set = {normalize_skill(s) for s in required_skills}

    matched = [
        skill for skill in required_skills
        if normalize_skill(skill) in user_set
    ]

    missing = [
        skill for skill in required_skills
        if normalize_skill(skill) not in user_set
    ]

    percentage = round(
        len(matched) / len(required_skills) * 100
    ) if required_skills else 0

    return percentage, matched, missing


def show_learning_resources(missing_skills):
    if not missing_skills:
        st.success("You have all the listed skills for this role!")
        return

    st.markdown("### 📚 Learning Resources for Missing Skills")
    st.write(
        "Use these resources to improve the skills required for your selected role."
    )

    for skill in missing_skills:
        with st.expander(f"🎯 Learn {skill}"):
            resources = RESOURCES.get(skill)

            if resources:
                for category, title, url in resources:
                    st.markdown(
                        f"- **{category}:** [{title}]({url})"
                    )
            else:
                st.markdown(
                    f"- [Search tutorials for {skill}]"
                    f"(https://www.youtube.com/results?search_query="
                    f"{skill.replace(' ', '+')}+tutorial)"
                )
                st.markdown(
                    f"- [Find courses for {skill}]"
                    f"(https://www.coursera.org/search?query="
                    f"{skill.replace(' ', '+')})"
                )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">💼 Skill-to-Job Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover suitable career paths, identify missing skills, '
    'and find learning resources.'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# DATASET SUMMARY - MAIN PAGE, WHITE TEXT
# --------------------------------------------------
st.markdown("""
<div class="dataset-summary-card">
    <div class="dataset-summary-title">📊 Dataset Summary</div>
    <div class="dataset-summary-text">
        ✅ 20 Job Roles<br>
        ✅ Expanded Skill Dataset<br>
        ✅ Job-Match Percentages<br>
        ✅ Missing-Skill Identification<br>
        ✅ Learning Websites and Videos<br>
        ✅ Courses and Certification Options
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATASET METRICS
# --------------------------------------------------
metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Total Job Roles", len(JOB_ROLES))

with metric2:
    st.metric("Unique Skills", len(ALL_SKILLS))

with metric3:
    st.metric("Learning Resource Topics", len(RESOURCES))

# --------------------------------------------------
# USER INPUT FORM
# --------------------------------------------------
st.markdown("## 👤 Enter Your Details")

with st.form("skill_matcher_form"):
    name = st.text_input("Your Name", placeholder="Enter your name")

    email = st.text_input(
        "Email (optional)",
        placeholder="Enter your email"
    )

    selected_role = st.selectbox(
        "Select Your Target Job Role",
        list(JOB_ROLES.keys())
    )

    selected_skills = st.multiselect(
        "Select the Skills You Already Know",
        ALL_SKILLS,
        help="Select all the technical and professional skills you have."
    )

    custom_skills_text = st.text_input(
        "Add Other Skills (optional)",
        placeholder="Example: C++, communication, problem solving"
    )

    submitted = st.form_submit_button(
        "🚀 Find My Job Match",
        use_container_width=True
    )

# --------------------------------------------------
# PROCESS INPUT AND SAVE RESULTS
# --------------------------------------------------
if submitted:
    custom_skills = [
        skill.strip()
        for skill in custom_skills_text.split(",")
        if skill.strip()
    ]

    # Match custom skills to known skill names without
    # requiring the user to type the exact capitalization.
    skill_lookup = {
        normalize_skill(skill): skill
        for skill in ALL_SKILLS
    }

    normalized_custom_skills = []
    for skill in custom_skills:
        normalized_custom_skills.append(
            skill_lookup.get(normalize_skill(skill), skill)
        )

    user_skills = list(dict.fromkeys(
        selected_skills + normalized_custom_skills
    ))

    if not user_skills:
        st.warning(
            "Please select at least one skill or enter a custom skill."
        )
        st.session_state.pop("match_result", None)
    else:
        percentage, matched, missing = calculate_match(
            user_skills,
            JOB_ROLES[selected_role]
        )

        st.session_state["match_result"] = {
            "name": name,
            "email": email,
            "role": selected_role,
            "user_skills": user_skills,
            "percentage": percentage,
            "matched": matched,
            "missing": missing
        }

# --------------------------------------------------
# DISPLAY MATCH RESULTS
# --------------------------------------------------
if st.session_state.get("match_result"):
    result = st.session_state["match_result"]

    st.divider()
    st.markdown("## 🎯 Your Job Match Results")

    if result["name"]:
        st.write(f"Hello, **{result['name']}!**")

    st.write(f"**Selected Job Role:** {result['role']}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Job Match Percentage",
            f"{result['percentage']}%"
        )

    with col2:
        st.metric(
            "Skills Matched",
            f"{len(result['matched'])}/{len(JOB_ROLES[result['role']])}"
        )

    st.progress(result["percentage"] / 100)

    if result["percentage"] >= 80:
        st.success(
            "Excellent match! You have most of the required skills."
        )
    elif result["percentage"] >= 50:
        st.info(
            "Good progress! Learn the missing skills to improve your match."
        )
    else:
        st.warning(
            "Keep learning! Focus on the missing skills listed below."
        )

    st.markdown("### ✅ Skills You Already Have")

    if result["matched"]:
        st.write(", ".join(result["matched"]))
    else:
        st.write("No required skills matched yet.")

    st.markdown("### ❗ Missing Skills to Learn")

    if result["missing"]:
        for skill in result["missing"]:
            st.write(f"🔹 {skill}")
    else:
        st.success("You have all the required skills in this dataset.")

    show_learning_resources(result["missing"])

    # --------------------------------------------------
    # LEARNING PLAN
    # --------------------------------------------------
    st.markdown("## 🗓️ Suggested Learning Plan")

    if result["missing"]:
        for index, skill in enumerate(result["missing"], start=1):
            st.write(f"**Step {index}:** Learn {skill} and practise it.")

        st.info(
            "Build a small project using each new skill and add it "
            "to your portfolio or GitHub profile."
        )
    else:
        st.success(
            "Focus on real-world projects, interview preparation, "
            "and building a strong portfolio."
        )

# --------------------------------------------------
# COMPARE JOB ROLES
# --------------------------------------------------
st.divider()
st.markdown("## 🔎 Compare Job Roles")

st.write(
    "Compare your current skills against other roles in the dataset."
)

if st.session_state.get("match_result"):
    comparison_skills = st.session_state["match_result"]["user_skills"]
else:
    comparison_skills = []

compare_roles = st.multiselect(
    "Choose roles to compare",
    list(JOB_ROLES.keys()),
    default=["Data Analyst", "Python Developer"]
)

if st.button("Compare Selected Roles", use_container_width=True):
    if not comparison_skills:
        st.warning(
            "Submit your skills in the form above before comparing roles."
        )
    elif not compare_roles:
        st.warning("Please select at least one job role.")
    else:
        comparison_results = []

        for role in compare_roles:
            percentage, matched, missing = calculate_match(
                comparison_skills,
                JOB_ROLES[role]
            )

            comparison_results.append({
                "Job Role": role,
                "Match %": percentage,
                "Matched Skills": ", ".join(matched) or "None",
                "Missing Skills": ", ".join(missing) or "None"
            })

        st.session_state["comparison_results"] = comparison_results

if st.session_state.get("comparison_results"):
    st.dataframe(
        st.session_state["comparison_results"],
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# CAREER GUIDANCE
# --------------------------------------------------
st.divider()
st.markdown("## 💡 Career Guidance")

st.markdown("""
- **Practise regularly:** Solve coding questions and complete hands-on exercises.
- **Build projects:** Apply your skills to practical problems.
- **Create a portfolio:** Upload suitable projects to GitHub.
- **Prepare for interviews:** Revise technical concepts and practise explaining projects.
- **Keep learning:** Review job descriptions to understand current industry requirements.
""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    "<p style='text-align:center;color:#cbd5e1 !important;'>"
    "Skill-to-Job Matcher | Career Guidance and Skill Development"
    "</p>",
    unsafe_allow_html=True
)
