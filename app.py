# app.py
import os
from datetime import datetime
import streamlit as st

# --- Google GenAI SDK ---
# Uses the new google-genai SDK (from google import genai)
from google import genai

# Optionally use python-dotenv to load .env in local dev
from dotenv import load_dotenv

load_dotenv()  # loads .env file if present

# Page configuration
st.set_page_config(
    page_title="Smart Cities & Green Buildings",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (original green-style UI preserved)
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #2E7D32;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #558B2F;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .info-box {
        background-color: #F1F8E9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Initialize GenAI client once (cached) ---
@st.cache_resource
def get_genai_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # Friendly instruction if the key is missing
        st.error(
            "GEMINI_API_KEY not found. Put your API key into a .env file (GEMINI_API_KEY=...) or export an env var."
        )
        st.stop()
    # Create client; pass api_key explicitly (recommended for quick-start)
    client = genai.Client(api_key=api_key)
    return client

client = get_genai_client()

# Helper: generate text
def generate_text(prompt: str, model_name: str = "gemini-2.5-flash"):
    """
    Generate text using the google genai client.
    Returns response.text (string).
    """
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        # bubble up a readable message
        return f"[ERROR] {str(e)}"

# Header
st.markdown('<p class="main-header">🏙️ SMART CITIES & GREEN BUILDINGS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Innovating for a Sustainable Tomorrow</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/city.png", width=80)
    st.title("Navigation")

    page = st.radio(
        "Select a section:",
        ["🏠 Home", "💡 Smart Solutions", "🌱 Green Technologies", "🤖 AI Assistant", "📊 Analytics"],
    )

    st.divider()
    st.markdown("### 🎓 Institution Info")
    st.markdown("**Ajeenkya DY Patil School of Engineering, Lohegaon, Pune**")
    st.markdown("*Affiliated to Savitribai Phule Pune University*")

# --- Pages ---
if page == "🏠 Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌍 Key Focus Areas")
        st.markdown(
            """
            - **Smart Infrastructure**: IoT-enabled urban systems
            - **Green Buildings**: Energy-efficient architecture
            - **Sustainable Transport**: Electric & public transit
            - **Waste Management**: Smart recycling solutions
            - **Energy Systems**: Renewable energy integration
            - **Water Conservation**: Smart water management
            """
        )
    with col2:
        st.markdown("### 🎯 Project Goals")
        st.markdown(
            """
            - Reduce carbon emissions by 50%
            - Achieve 80% energy efficiency
            - Implement 100% renewable energy
            - Zero waste to landfill target
            - Smart mobility for all citizens
            - Improve quality of life metrics
            """
        )

    st.divider()
    st.markdown("### 🔄 Real-time Urban Sustainability Insights")

    if st.button("🔍 Get Latest Insights from AI"):
        with st.spinner("Analyzing current trends..."):
            prompt = (
                "Provide 3 brief, current insights about smart cities and green buildings. "
                "Each insight should be 1-2 sentences. Focus on recent innovations, technologies, or trends. "
                "Format as JSON with keys: insight1, insight2, insight3"
            )
            output = generate_text(prompt)
            if output.startswith("[ERROR]"):
                st.error(output)
            else:
                st.success("✅ Latest insights generated!")
                st.markdown(f"**AI-Generated Insights ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})**")
                st.info(output)

elif page == "💡 Smart Solutions":
    st.header("💡 Smart City Solutions")
    solution_type = st.selectbox(
        "Select solution category:",
        ["Smart Energy", "Smart Mobility", "Smart Buildings", "Smart Waste", "Smart Water"],
    )
    if st.button("🚀 Generate Solution Ideas"):
        with st.spinner("Generating innovative solutions..."):
            prompt = (
                f"Generate 5 innovative {solution_type} solutions for smart cities. "
                "For each solution, provide:\n"
                "1. Solution name\n"
                "2. Brief description (2-3 sentences)\n"
                "3. Key technology used\n"
                "4. Expected impact\n\nFormat as a numbered list."
            )
            output = generate_text(prompt)
            if output.startswith("[ERROR]"):
                st.error(output)
            else:
                st.success("✅ Solutions generated!")
                st.markdown(output)

elif page == "🌱 Green Technologies":
    st.header("🌱 Green Building Technologies")
    col1, col2 = st.columns(2)
    with col1:
        building_type = st.selectbox(
            "Building Type:", ["Residential", "Commercial", "Industrial", "Educational", "Healthcare"]
        )
    with col2:
        climate_zone = st.selectbox("Climate Zone:", ["Tropical", "Arid", "Temperate", "Cold", "Polar"])
    if st.button("🌿 Get Green Technology Recommendations"):
        with st.spinner("Analyzing optimal green technologies..."):
            prompt = (
                f"Recommend 5 specific green building technologies for a {building_type} building in a {climate_zone} climate. "
                "For each technology:\n"
                "1. Technology name\n"
                "2. How it works\n"
                "3. Energy savings potential\n"
                "4. Cost-effectiveness\n"
                "5. Implementation difficulty\n\nBe specific and practical."
            )
            output = generate_text(prompt)
            if output.startswith("[ERROR]"):
                st.error(output)
            else:
                st.success("✅ Recommendations ready!")
                st.markdown(output)
                st.divider()
                c1, c2, c3 = st.columns(3)
                c1.metric("Potential Energy Savings", "40-60%", "+15%")
                c2.metric("ROI Period", "5-7 years", "-2 years")
                c3.metric("Carbon Reduction", "45%", "+12%")

elif page == "🤖 AI Assistant":
    st.header("🤖 AI Sustainability Assistant")
    st.markdown("Ask questions about smart cities, green buildings, and sustainable urban development!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("Ask about smart cities and green buildings..."):
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                prompt = (
                    "You are an expert in smart cities and green buildings. "
                    f"Answer this question professionally and practically: {user_question}\n\n"
                    "Provide actionable insights and real-world examples where relevant."
                )
                output = generate_text(prompt)
                if output.startswith("[ERROR]"):
                    st.error(output)
                else:
                    st.markdown(output)
                    st.session_state.messages.append({"role": "assistant", "content": output})

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()

elif page == "📊 Analytics":
    st.header("📊 Sustainability Analytics Dashboard")
    analysis_type = st.radio(
        "Select Analysis Type:", ["City Comparison", "Technology ROI", "Impact Assessment", "Future Trends"]
    )

    if analysis_type == "City Comparison":
        cities = st.multiselect(
            "Select cities to compare:",
            [
                "Singapore",
                "Copenhagen",
                "Amsterdam",
                "Barcelona",
                "San Francisco",
                "Tokyo",
                "Dubai",
                "Stockholm",
                "Oslo",
                "Vienna",
            ],
            default=["Singapore", "Copenhagen"],
        )
        if st.button("📈 Compare Cities"):
            with st.spinner("Analyzing cities..."):
                prompt = (
                    f"Compare these cities in terms of smart city and green building initiatives: {', '.join(cities)}\n\n"
                    "Provide:\n1. Overall sustainability ranking\n2. Key strengths of each city\n3. Innovative technologies used\n4. Lessons learned\n5. Best practices to adopt\n\nBe specific with examples."
                )
                output = generate_text(prompt)
                if output.startswith("[ERROR]"):
                    st.error(output)
                else:
                    st.success("✅ Analysis complete!")
                    st.markdown(output)

    elif analysis_type == "Technology ROI":
        tech = st.selectbox(
            "Select Technology:",
            ["Solar Panels", "Smart HVAC", "Rainwater Harvesting", "LED Lighting", "Green Roofs", "Energy Storage", "Smart Windows", "Geothermal Cooling"],
        )
        investment = st.number_input("Investment Amount (USD):", min_value=1000, value=50000, step=1000)
        if st.button("💰 Calculate ROI"):
            with st.spinner("Calculating returns..."):
                prompt = (
                    f"Calculate detailed ROI for {tech} with an investment of ${investment}.\n\n"
                    "Include:\n1. Payback period\n2. Annual savings\n3. 10-year cost-benefit analysis\n4. Environmental impact (CO2 reduction)\n5. Maintenance costs\n6. Risk factors\n\nUse realistic industry averages."
                )
                output = generate_text(prompt)
                if output.startswith("[ERROR]"):
                    st.error(output)
                else:
                    st.success("✅ ROI calculated!")
                    st.markdown(output)

    elif analysis_type == "Impact Assessment":
        st.markdown("### 🌍 Environmental Impact Assessment")
        scenario = st.text_area(
            "Describe your smart city/green building scenario:",
            placeholder="E.g., Converting 100 buildings to net-zero energy in a city of 500,000 people...",
        )
        if st.button("🔬 Assess Impact") and scenario:
            with st.spinner("Assessing environmental impact..."):
                prompt = (
                    f"Conduct a detailed environmental impact assessment for: {scenario}\n\n"
                    "Analyze:\n1. Carbon emission reduction (tons/year)\n2. Energy savings (MWh/year)\n3. Water conservation (gallons/year)\n4. Cost savings (USD/year)\n5. Job creation potential\n6. Social benefits\n7. Implementation challenges\n\nProvide specific numbers and calculations."
                )
                output = generate_text(prompt)
                if output.startswith("[ERROR]"):
                    st.error(output)
                else:
                    st.success("✅ Impact assessed!")
                    st.markdown(output)

    else:  # Future Trends
        timeframe = st.slider("Select timeframe (years ahead):", 1, 20, 10)
        if st.button("🔮 Predict Future Trends"):
            with st.spinner("Analyzing future trends..."):
                prompt = (
                    f"Predict smart city and green building trends for the next {timeframe} years.\n\n"
                    "Cover:\n1. Emerging technologies\n2. Policy changes expected\n3. Market evolution\n4. Consumer behavior shifts\n5. Major challenges ahead\n6. Investment opportunities\n7. Breakthrough innovations likely\n\nBe forward-thinking but realistic."
                )
                output = generate_text(prompt)
                if output.startswith("[ERROR]"):
                    st.error(output)
                else:
                    st.success("✅ Trends identified!")
                    st.markdown(output)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Ajeenkya DY Patil School of Engineering, Lohegaon, Pune</strong></p>
        <p>Empowerment through quality technical education</p>
        <p>Approved by AICTE, Affiliated to Savitribai Phule Pune University</p>
    </div>
    """,
    unsafe_allow_html=True,
)
