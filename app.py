# app.py
import os
from datetime import datetime
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Smart Cities & Green Buildings — Research & Solutions",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =======================
#   THEME (LIGHT + DARK)
# =======================
st.markdown(
    """
<style>

/* -----------------------
   LIGHT MODE (Default)
------------------------*/
:root {
    --brand-primary: #89A8B2;      /* soft gray-blue */
    --brand-accent:  #97C4B8;      /* soft teal */
    --muted:         #8A939B;      /* gray muted text */
    --panel-bg:      #F3F5F6;      /* light card */
    --page-bg:       #FFFFFF;      /* light background */
    --border:        rgba(0,0,0,0.06);
    --radius:        10px;
    --card-padding:  16px;
    --font-sans:     "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* -----------------------
   DARK MODE (Auto)
------------------------*/
@media (prefers-color-scheme: dark) {
    :root {
        --brand-primary: #A8CED4;      /* pastel blue */
        --brand-accent:  #8AC7B8;      /* pastel teal */
        --muted:         #B8C2C8;
        --panel-bg:      #2A2D31;      /* dark card */
        --page-bg:       #1C1F22;      /* dark background */
        --border:        rgba(255,255,255,0.08);
    }
}

/* Page Background */
.reportview-container, .main {
    background-color: var(--page-bg);
    font-family: var(--font-sans);
    color: var(--brand-primary);
}

/* Headings */
.main-header {
    font-size: 1.9rem;
    color: var(--brand-primary);
    font-weight: 700;
    margin-bottom: 4px;
}
.sub-header {
    font-size: 1.05rem;
    color: var(--muted);
    margin-bottom: 12px;
}

/* Cards / Panels */
.info-box {
    background-color: var(--panel-bg);
    padding: var(--card-padding);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    margin: 12px 0;
}

/* Buttons */
.stButton>button {
    background-color: var(--brand-accent) !important;
    color: #fff !important;
    font-weight: 600;
    border-radius: 8px;
    padding: 8px 14px;
    border: none;
}
.stButton>button:hover {
    filter: brightness(1.05);
}

/* Muted text */
.small-muted {
    color: var(--muted);
}

/* Metrics */
.metric {
    padding: 12px 8px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =======================
#   INIT GEMINI CLIENT
# =======================
@st.cache_resource
def get_genai_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("API key not found. Add GEMINI_API_KEY to .env")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_genai_client()

def generate_text(prompt, model_name="gemini-2.5-flash"):
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        return f"[ERROR] {e}"


# HEADER
st.markdown('<div class="main-header">SMART CITIES & GREEN BUILDINGS — Research & Solutions</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Practical approaches for sustainable urban development and building performance.</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/96/000000/city.png", width=70)
    st.title("Navigation")

    page = st.radio(
        "Section:",
        ["Home", "Smart Solutions", "Green Technologies", "AI Assistant", "Analytics"],
    )

    st.divider()
    st.markdown("### Institution")
    st.markdown("**Ajeenkya DY Patil School of Engineering, Lohegaon, Pune**")
    st.markdown("Affiliated to Savitribai Phule Pune University")
    st.markdown("<div class='small-muted'>Approved by AICTE</div>", unsafe_allow_html=True)


# =======================
#        PAGES
# =======================

# HOME PAGE
if page == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Key Focus Areas")
        st.markdown(
            """
            - Smart infrastructure & IoT systems  
            - Energy-efficient building design  
            - Sustainable mobility systems  
            - Waste & water management  
            - Renewable energy integration  
            """
        )
    with col2:
        st.markdown("### Project Objectives")
        st.markdown(
            """
            - Reduce carbon emissions  
            - Increase renewable adoption  
            - Enhance urban livability  
            - Build scalable, future-ready solutions  
            """
        )

    st.divider()
    st.markdown("### Real-time Urban Sustainability Insights")

    if st.button("Get AI insights"):
        with st.spinner("Generating insights..."):
            prompt = (
                "Provide 3 concise insights about smart cities and green buildings. "
                "Each 1–2 sentences. Return as JSON keys: insight1, insight2, insight3."
            )
        res = generate_text(prompt)
        st.info(res)


# SMART SOLUTIONS
elif page == "Smart Solutions":
    st.header("Smart City Solutions")
    category = st.selectbox("Solution category:", ["Smart Energy", "Smart Mobility", "Smart Buildings", "Smart Waste", "Smart Water"])

    if st.button("Generate solution ideas"):
        prompt = f"""
        Generate 5 practical {category} solutions for smart cities.
        For each:
        1. Name
        2. 2–3 sentence practical explanation
        3. Tech used
        4. Expected impact
        """
        st.markdown(generate_text(prompt))


# GREEN TECHNOLOGIES
elif page == "Green Technologies":
    st.header("Green Building Technologies")
    col1, col2 = st.columns(2)
    with col1:
        btype = st.selectbox("Building type:", ["Residential", "Commercial", "Industrial", "Educational", "Healthcare"])
    with col2:
        climate = st.selectbox("Climate zone:", ["Tropical", "Arid", "Temperate", "Cold", "Polar"])

    if st.button("Get recommendations"):
        prompt = f"""
        Recommend 5 green building technologies for a {btype} building in a {climate} climate.
        Include:
        - Technology name
        - How it works
        - Energy saving value
        - Cost effectiveness
        - Implementation difficulty
        """
        st.markdown(generate_text(prompt))


# AI ASSISTANT
elif page == "AI Assistant":
    st.header("AI Sustainability Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user := st.chat_input("Ask anything about smart cities..."):
        st.session_state.chat.append({"role": "user", "content": user})

        with st.chat_message("assistant"):
            reply = generate_text(
                f"You are an expert sustainability consultant. Answer: {user}"
            )
            st.session_state.chat.append({"role": "assistant", "content": reply})
            st.markdown(reply)


# ANALYTICS PAGE
elif page == "Analytics":
    st.header("Sustainability Analytics Dashboard")

    atype = st.radio("Select analysis type:", ["City Comparison", "Technology ROI", "Impact Assessment", "Future Trends"])

    if atype == "City Comparison":
        cities = st.multiselect("Select cities:", ["Singapore", "Copenhagen", "Amsterdam", "Tokyo", "Dubai"], default=["Singapore", "Copenhagen"])
        if st.button("Compare"):
            prompt = f"Compare these cities on sustainability: {cities}. Provide ranking, strengths, innovations, lessons."
            st.markdown(generate_text(prompt))

    elif atype == "Technology ROI":
        tech = st.selectbox("Technology:", ["Solar Panels", "Smart HVAC", "Rainwater Harvesting", "Green Roofs"])
        invest = st.number_input("Investment (USD):", value=50000)
        if st.button("Calculate ROI"):
            prompt = f"Calculate ROI for {tech} given investment {invest}. Include payback, yearly savings, CO2 reduction."
            st.markdown(generate_text(prompt))

    elif atype == "Impact Assessment":
        scenario = st.text_area("Describe scenario:")
        if st.button("Assess Impact"):
            prompt = f"Perform environmental impact assessment for scenario: {scenario}"
            st.markdown(generate_text(prompt))

    else:
        years = st.slider("Years ahead:", 1, 20, 10)
        if st.button("Predict Trends"):
            prompt = f"Predict smart city and green building trends for next {years} years."
            st.markdown(generate_text(prompt))


# FOOTER
st.divider()
st.markdown(
    """
<div style='text-align:center; color:var(--muted); padding: 10px;'>
    <strong>Ajeenkya DY Patil School of Engineering, Lohegaon, Pune</strong><br>
    Empowering future-ready sustainable innovation<br>
    Approved by AICTE • Affiliated to Savitribai Phule Pune University
</div>
""",
    unsafe_allow_html=True,
)
