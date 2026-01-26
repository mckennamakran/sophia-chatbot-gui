import streamlit as st
import pandas as pd
import os
import csv

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Sophia — Relapse Prevention Assistant",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DARK MODE THEME - BLACK BACKGROUND, PINK ACCENTS ONLY
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff;
    }
    
    /* Main containers */
    .main > div {
        background-color: #000000;
    }
    
    /* Headers with pink gradient */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 600;
    }
    
    h1 {
        background: linear-gradient(90deg, #E0218A 0%, #FF6EC7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Text color */
    p, div, span {
        color: #ffffff !important;
    }
    
    /* Input fields - dark with pink border */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
        border-radius: 10px;
        padding: 0.75em;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #E0218A !important;
        box-shadow: 0 0 0 2px rgba(224, 33, 138, 0.2) !important;
    }
    
    /* Multi-select styling - PINK */
    .stMultiSelect > div > div {
        background-color: #111111 !important;
        border-color: #333333 !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #E0218A !important;
    }
    
    /* Selected items in multiselect - PINK */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(224, 33, 138, 0.2) !important;
        color: #FF6EC7 !important;
        border-color: #E0218A !important;
    }
    
    /* Pink buttons */
    .stButton>button {
        background: linear-gradient(135deg, #E0218A 0%, #c91b78 100%);
        color: white !important;
        border-radius: 12px;
        padding: 0.7em 1.4em;
        border: none;
        font-size: 16px;
        font-weight: 500;
        margin-top: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(224, 33, 138, 0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(224, 33, 138, 0.4);
        background: linear-gradient(135deg, #c91b78 0%, #E0218A 100%);
        color: white;
    }
    
    /* Pink sliders */
    div[data-baseweb="slider"] > div > div > div > div {
        background: linear-gradient(90deg, #E0218A 0%, #FF6EC7 100%) !important;
    }
    
    div[data-baseweb="slider"] span {
        background: linear-gradient(135deg, #E0218A 0%, #FF6EC7 100%) !important;
        border-color: #E0218A !important;
        box-shadow: 0 2px 8px rgba(224, 33, 138, 0.3);
    }
    
    /* Dark containers with pink accents */
    .dark-container {
        background-color: #111111;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #E0218A;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E0218A, transparent);
        margin: 2rem 0;
    }
    
    /* Pink info notes */
    .info-note {
        background-color: rgba(224, 33, 138, 0.1);
        border-left: 3px solid #E0218A;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #FFB6D9 !important;
    }
    
    /* Pink warning boxes */
    .warning-box {
        background-color: rgba(224, 33, 138, 0.15);
        border-left: 4px solid #FF6EC7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #FFB6D9 !important;
    }
    
    /* Progress indicator - pink */
    .progress-container {
        margin: 2rem 0;
    }
    
    .progress-step {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #333333;
        margin: 0 6px;
        transition: all 0.3s ease;
    }
    
    .progress-step.active {
        background: linear-gradient(135deg, #E0218A 0%, #FF6EC7 100%);
        transform: scale(1.3);
        box-shadow: 0 0 0 3px rgba(224, 33, 138, 0.2);
    }
    
    /* Results card */
    .result-card {
        background: linear-gradient(135deg, #111111 0%, #1a1a1a 100%);
        border: 2px solid #333333;
        border-left: 4px solid #E0218A;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    /* Status indicators - PINK variations (NO RED) */
    .status-low { 
        color: #FF6EC7 !important; 
        font-weight: 600; 
        background: rgba(255, 110, 199, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
    }
    .status-medium { 
        color: #E0218A !important; 
        font-weight: 600; 
        background: rgba(224, 33, 138, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
    }
    .status-high { 
        color: #FF1493 !important; 
        font-weight: 600; 
        background: rgba(255, 110, 199, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
    }
    
    /* Custom checkbox styling */
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Radio buttons */
    div[data-baseweb="radio"] > div {
        background-color: #111111;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    
    /* Therapeutic explanation boxes */
    .therapy-box {
        background-color: rgba(224, 33, 138, 0.05);
        border: 1px solid rgba(224, 33, 138, 0.2);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #FFB6D9 !important;
        font-style: italic;
    }
    
    /* Large number display for results */
    .big-number {
        font-size: 4em;
        font-weight: 700;
        background: linear-gradient(90deg, #E0218A 0%, #FF6EC7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Pink pill badges - horizontal layout */
    .pill-badge {
        background: rgba(224, 33, 138, 0.2);
        color: #FF6EC7 !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 0.3rem;
        display: inline-block;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #E0218A;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF6EC7;
    }
    
    /* Trigger section headers */
    .section-header {
        color: #FF6EC7;
        font-size: 1.2em;
        font-weight: 600;
        margin: 1.5rem 0 0.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(224, 33, 138, 0.3);
    }
    
    /* Intensity display box */
    .intensity-box {
        background: #111111;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #333333;
    }
    
    /* Slider value display */
    .slider-value {
        font-size: 2em;
        color: #FF6EC7;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    /* Horizontal pill container */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION STATE MANAGEMENT
# =========================================================
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# =========================================================
# DATA DEFINITIONS (EXACTLY FROM ORIGINAL CODE)
# =========================================================
ADDICTION_GROUPS = {
    1: {
        'group_name': 'Cannabis',
        'drugs': {
            'a': 'Marijuana',
            'b': 'Hashish',
            'c': 'Other cannabis-containing substances'
        }
    },
    2: {
        'group_name': 'Synthetic cannabinoids',
        'drugs': {
            'a': 'K2',
            'b': 'Spice',
            'c': 'Bath salts'
        }
    },
    3: {
        'group_name': 'Sedatives',
        'drugs': {
            'a': 'Barbiturates',
            'b': 'Benzodiazepines',
            'c': 'Hypnotics'
        }
    },
    4: {
        'group_name': 'Stimulants',
        'drugs': {
            'a': 'Methamphetamine',
            'b': 'Cocaine',
            'c': 'Other stimulants'
        }
    },
    5: {
        'group_name': 'Club drugs',
        'drugs': {
            'a': 'MDMA (Ecstasy / Molly)',
            'b': 'GHB',
            'c': 'Ketamine',
            'd': 'Flunitrazepam (Rohypnol)'
        }
    },
    6: {
        'group_name': 'Hallucinogens',
        'drugs': {
            'a': 'LSD',
            'b': 'PCP',
            'c': 'Other hallucinogens'
        }
    },
    7: {
        'group_name': 'Inhalants',
        'drugs': {
            'a': 'Glue',
            'b': 'Paint thinners',
            'c': 'Correction fluid',
            'd': 'Marker fluid',
            'e': 'Gasoline',
            'f': 'Cleaning fluids',
            'g': 'Household aerosol products'
        }
    },
    8: {
        'group_name': 'Opioids',
        'drugs': {
            'a': 'Heroin',
            'b': 'Morphine',
            'c': 'Codeine',
            'd': 'Methadone',
            'e': 'Fentanyl',
            'f': 'Oxycodone'
        }
    }
}

TRIGGERS = {
    'Emotional Triggers': {
        'a': 'Stress',
        'b': 'Anxiety',
        'c': 'Depression',
        'd': 'Loneliness',
        'e': 'Anger',
        'f': 'Boredom',
        'g': 'Guilt or shame',
        'h': 'Low self-esteem',
        'i': 'Grief or loss',
        'j': 'Feeling overwhelmed'
    },
    'Mental Triggers': {
        'a': 'Cravings',
        'b': 'Obsessive thoughts',
        'c': 'Rationalizing use',
        'd': 'Minimizing consequences',
        'e': 'Negative self-talk',
        'f': 'Hopelessness',
        'g': 'Overconfidence in control'
    },
    'Environmental Triggers': {
        'a': 'Being around substances',
        'b': 'Certain places',
        'c': 'Easy access to drugs',
        'd': 'Lack of structure',
        'e': 'Being alone too long',
        'f': 'Parties or social events'
    },
    'Social Triggers': {
        'a': 'Peer pressure',
        'b': 'Conflict with others',
        'c': 'Feeling judged',
        'd': 'Relationship problems',
        'e': 'Isolation',
        'f': 'Enabling friends or family'
    }
}

CRAVING_TYPES = [
    'Physical urge',
    'Mental obsession',
    'Emotional craving',
    'Habit-based craving',
    'Stress-induced craving',
    'None'
]

MENTAL_HEALTH_CONDITIONS = [
    'Depression',
    'Anxiety',
    'PTSD',
    'Bipolar disorder',
    'ADHD',
    'Personality Disorder',
    'Other',
    'None'
]

LIFE_STRESSORS = [
    'Financial problems',
    'Work or school stress',
    'Relationship issues',
    'Health problems',
    'Legal issues',
    'Recent loss or grief',
    'None'
]

SUPPORT_OPTIONS = [
    'Family',
    'Friends',
    'Support group',
    'Therapist',
    'None'
]

GENDER_OPTIONS = ["", "Male", "Female", "Non-binary", "Prefer not to say"]

# =========================================================
# THERAPEUTIC EXPLANATIONS
# =========================================================
THERAPY_EXPLANATIONS = {
    'triggers': """
    <div class='therapy-box'>
    <b>Understanding Triggers:</b> Triggers are situations, emotions, or thoughts that can make you want to use or relapse. 
    Identifying them helps you prepare coping strategies. It's normal to have triggers—what matters is how you respond to them.
    </div>
    """,
    
    'intensity': """
    <div class='therapy-box'>
    <b>About Intensity Levels:</b> These scales help us understand the current state of your cravings, stress, and accessibility. 
    Being honest about these levels helps create a more accurate support plan.
    </div>
    """
}

# =========================================================
# UTILITY FUNCTIONS
# =========================================================
def next_step():
    st.session_state.current_step += 1
    st.rerun()

def prev_step():
    if st.session_state.current_step > 0:
        st.session_state.current_step -= 1
    st.rerun()

def reset_app():
    st.session_state.current_step = 0
    st.session_state.user_data = {}
    st.rerun()

def show_progress():
    steps = ["Welcome", "Basic Info", "Addiction", "Triggers", "Intensity Levels", 
             "Medication", "Self-Esteem", "Mental Health", "Life Stressors", 
             "Support", "Results"]
    
    current = st.session_state.current_step
    if current >= len(steps):
        current = len(steps) - 1
    
    progress_html = f"""
    <div class="progress-container">
        <div style="text-align: center; margin-bottom: 1rem; color: #FF6EC7; font-size: 0.9em;">
            Step {current + 1} of {len(steps)}: {steps[current]}
        </div>
        <div style="text-align: center;">
    """
    
    for i in range(len(steps)):
        if i <= current:
            progress_html += '<span class="progress-step active"></span>'
        else:
            progress_html += '<span class="progress-step"></span>'
    
    progress_html += "</div></div>"
    st.markdown(progress_html, unsafe_allow_html=True)

def store_data(user_data):
    """Store user data to CSV - exactly like original"""
    FILE_NAME = 'sophia_dataset.csv'
    column_names = [
        'first_name', 'surname', 'age', 'gender', 'addiction_type', 'triggers',
        'cravings', 'craving_intensity', 'accessibility_or_exposure', 'medication',
        'stress_levels', 'self_esteem', 'mental_health_conditions', 'life_stressors',
        'support', 'relapse_phase', 'prob_of_relapse'
    ]

    file_exists = os.path.exists(FILE_NAME)

    if not file_exists:
        empty_df = pd.DataFrame(columns=column_names)
        empty_df.to_csv(FILE_NAME, index=False)

    # Add new user data
    with open(FILE_NAME, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writerow(user_data)

def predict_relapse_risk(user_data):
    """Simulate ML prediction - exactly like original logic"""
    risk_score = 0
    
    # Factors from original logic
    stress = user_data.get('stress_levels', 5)
    cravings = user_data.get('craving_intensity', 5)
    access = user_data.get('accessibility_or_exposure', 0)
    support = user_data.get('support', 'None')
    self_esteem = user_data.get('self_esteem', 6)
    
    # Calculate risk
    risk_score += (stress / 10) * 0.25
    risk_score += (cravings / 10) * 0.25
    risk_score += (access / 5) * 0.20
    
    # Support system impact
    if isinstance(support, list):
        support_factor = 1 if 'None' in support else (1 - (len(support) * 0.2))
    else:
        support_factor = 1 if support == 'None' else 0.5
    
    risk_score += support_factor * 0.15
    
    # Self-esteem impact (lower = higher risk)
    risk_score += ((12 - self_esteem) / 12) * 0.15
    
    # Determine phase
    if risk_score < 0.3:
        phase = "low"
        prob = 0.2 + (risk_score * 0.2)
    elif risk_score < 0.7:
        phase = "medium"
        prob = 0.4 + ((risk_score - 0.3) * 0.3)
    else:
        phase = "high"
        prob = 0.7 + ((risk_score - 0.7) * 0.3)
    
    return phase, round(min(prob, 0.95), 2)

# =========================================================
# STEP 0: INTRODUCTION
# =========================================================
if st.session_state.current_step == 0:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0;">
        <div style="font-size: 4em; margin-bottom: 1rem; color: #E0218A;">🌸</div>
        <h1>Sophia</h1>
        <p style="color: #FFB6D9; font-size: 1.1em; max-width: 600px; margin: 0 auto;">
        Your compassionate companion for relapse prevention and recovery support
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dark-container">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 1.5em; margin-right: 0.5rem; color: #FF6EC7;">🤍</div>
            <h3 style="margin: 0; color: #ffffff;">Welcome</h3>
        </div>
        <p style="color: #cccccc; line-height: 1.6;">
        Hi, I'm <span style="color: #FF6EC7; font-weight: 500;">Sophia</span>. I'm here to support you on your recovery journey. 
        I'm going to walk you through a few questions about your experiences and feelings, 
        so I can give you more personalized guidance.
        </p>
        <div class="info-note">
        <b>🌸 Important:</b> This is a reflective check-in tool, not a diagnosis or replacement 
        for professional medical care. Always consult with healthcare professionals for medical advice.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Begin Assessment 🌷", use_container_width=True):
            next_step()

# =========================================================
# STEP 1: BASIC INFORMATION
# =========================================================
elif st.session_state.current_step == 1:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">👤 Basic Information</h3>
        <p style="color: #FFB6D9;">
        First, let's start with some basic information so I can better understand your situation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", key="first_name")
            age = st.number_input("Age", min_value=1, max_value=120, value=25, key="age")
        
        with col2:
            surname = st.text_input("Last Name", key="surname")
            gender = st.selectbox("Gender", GENDER_OPTIONS, key="gender")
    
    if first_name and surname and gender and age > 0:
        st.session_state.user_data.update({
            "first_name": first_name,
            "surname": surname,
            "age": age,
            "gender": gender.lower()
        })
        
        st.markdown(f"""
        <div class="info-note">
        ✨ Nice to meet you, {first_name}. Let's dive straight into it.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Next →", use_container_width=True):
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please fill in all the fields to continue.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 2: ADDICTION INFORMATION
# =========================================================
elif st.session_state.current_step == 2:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">💊 Addiction Information</h3>
        <p style="color: #FFB6D9;">
        What type of addiction do you have? Choose 1 from the list below.
        </p>
        <div class="info-note">
        <b>Note:</b> This program focuses on one addiction at a time. 
        If you want to work on another, you can complete another assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Convert addiction groups to user-friendly format
    group_options = [""] + [f"{k}. {v['group_name']}" for k, v in ADDICTION_GROUPS.items()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        group_display = st.selectbox("Substance Group (1-8)", group_options, key="group_select")
        
        if group_display:
            group_choice = int(group_display.split(".")[0])
            selected_group = ADDICTION_GROUPS[group_choice]
        else:
            group_choice = None
            selected_group = None
    
    with col2:
        if group_choice:
            drug_options = [""] + [f"{k}. {v}" for k, v in selected_group['drugs'].items()]
            drug_display = st.selectbox("Specific Substance", drug_options, key="drug_select")
            
            if drug_display:
                drug_choice = drug_display.split(".")[0]
                selected_drug = selected_group['drugs'][drug_choice]
            else:
                drug_choice = None
                selected_drug = None
        else:
            st.selectbox("Specific Substance", [""], disabled=True, key="drug_disabled")
    
    if group_choice and drug_choice:
        addiction_type = f"{selected_group['group_name']} -> {selected_drug}"
        st.session_state.user_data["addiction_type"] = addiction_type
        
        st.markdown(f"""
        <div class="info-note">
        ✨ Thank you for sharing. Now let's explore your triggers.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Next →", use_container_width=True):
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please select both the substance group and specific substance.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 3: TRIGGERS (ALL IN ONE SECTION WITH MULTISELECT FOR EACH TYPE)
# =========================================================
elif st.session_state.current_step == 3:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">⚡ Triggers Assessment</h3>
        <p style="color: #FFB6D9;">
        Understanding your triggers helps you prepare for challenging moments.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Therapeutic explanation
    st.markdown(THERAPY_EXPLANATIONS['triggers'], unsafe_allow_html=True)
    
    all_selected_triggers = []
    
    # Emotional Triggers
    st.markdown('<div class="section-header">🎭 Emotional Triggers</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    Feelings and emotional states that might lead to cravings
    </div>
    """, unsafe_allow_html=True)
    
    emotional_triggers = list(TRIGGERS['Emotional Triggers'].values())
    selected_emotional = st.multiselect(
        "Select emotional triggers:",
        emotional_triggers,
        key="emotional_triggers",
        help="Select all that apply"
    )
    all_selected_triggers.extend(selected_emotional)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Mental Triggers
    st.markdown('<div class="section-header">💭 Mental Triggers</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    Thoughts and thinking patterns that can lead to cravings
    </div>
    """, unsafe_allow_html=True)
    
    mental_triggers = list(TRIGGERS['Mental Triggers'].values())
    selected_mental = st.multiselect(
        "Select mental triggers:",
        mental_triggers,
        key="mental_triggers",
        help="Select all that apply"
    )
    all_selected_triggers.extend(selected_mental)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Environmental Triggers
    st.markdown('<div class="section-header">📍 Environmental Triggers</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    Places, situations, or environmental factors that can trigger cravings
    </div>
    """, unsafe_allow_html=True)
    
    environmental_triggers = list(TRIGGERS['Environmental Triggers'].values())
    selected_environmental = st.multiselect(
        "Select environmental triggers:",
        environmental_triggers,
        key="environmental_triggers",
        help="Select all that apply"
    )
    all_selected_triggers.extend(selected_environmental)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Social Triggers
    st.markdown('<div class="section-header">👥 Social Triggers</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    People and social situations that can trigger cravings
    </div>
    """, unsafe_allow_html=True)
    
    social_triggers = list(TRIGGERS['Social Triggers'].values())
    selected_social = st.multiselect(
        "Select social triggers:",
        social_triggers,
        key="social_triggers",
        help="Select all that apply"
    )
    all_selected_triggers.extend(selected_social)
    
    # Show selected triggers summary - HORIZONTAL LAYOUT
    if all_selected_triggers:
        st.markdown("""
        <div class="dark-container">
            <h4 style="color: #FF6EC7;">✅ Selected Triggers Summary</h4>
            <div class="pill-container">
        """, unsafe_allow_html=True)
        
        for trigger in all_selected_triggers:
            st.markdown(f'<span class="pill-badge">{trigger}</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
            </div>
            <div style="margin-top: 1rem; color: #FFB6D9;">
            Total triggers selected: <b>{len(all_selected_triggers)}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back", use_container_width=True):
            prev_step()
    with col3:
        if st.button("Next →", use_container_width=True):
            if all_selected_triggers:
                st.session_state.user_data['triggers'] = ', '.join(all_selected_triggers)
                st.markdown("""
                <div class="info-note">
                ✨ Great job identifying your triggers! Now let's assess your current intensity levels.
                </div>
                """, unsafe_allow_html=True)
                next_step()
            else:
                st.markdown("""
                <div class="warning-box">
                💗 Please select at least one trigger to continue.
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# STEP 4: INTENSITY LEVELS (CRAVINGS, STRESS, ACCESSIBILITY IN ONE PAGE)
# =========================================================
elif st.session_state.current_step == 4:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">📊 Intensity Levels Assessment</h3>
        <p style="color: #FFB6D9;">
        Let's assess your current craving intensity, stress levels, and accessibility.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Therapeutic explanation
    st.markdown(THERAPY_EXPLANATIONS['intensity'], unsafe_allow_html=True)
    
    # Cravings Section
    st.markdown('<div class="section-header">💭 Cravings Intensity</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    Rate your current craving intensity from 0-10
    </div>
    """, unsafe_allow_html=True)
    
    craving_intensity = st.slider(
        "Craving Intensity (0 = No craving, 10 = Extreme craving)",
        min_value=0,
        max_value=10,
        value=5,
        key="craving_intensity_slider"
    )
    
    # Display craving intensity
    craving_levels = ["No craving", "Very mild", "Mild", "Mild to moderate", "Moderate", 
                      "Moderate to high", "High", "Very high", "Severe", "Very severe", "Extreme"]
    craving_color = "#FF6EC7" if craving_intensity < 4 else ("#E0218A" if craving_intensity < 7 else "#FF1493")
    
    st.markdown(f"""
    <div class="intensity-box">
        <div class="slider-value" style="color: {craving_color};">{craving_intensity}/10</div>
        <div style="color: #FFB6D9;">{craving_levels[craving_intensity]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.user_data['craving_intensity'] = craving_intensity
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Stress Levels Section
    st.markdown('<div class="section-header">😰 Stress Levels</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    Rate your current stress level from 0-10
    </div>
    """, unsafe_allow_html=True)
    
    stress_level = st.slider(
        "Stress Level (0 = No stress, 10 = Extremely stressed)",
        min_value=0,
        max_value=10,
        value=5,
        key="stress_slider"
    )
    
    # Display stress level
    stress_levels = ["No stress", "Very mild", "Mild", "Mild to moderate", "Moderate", 
                     "Moderate to high", "High", "Very high", "Severe", "Very severe", "Extreme"]
    stress_color = "#FF6EC7" if stress_level < 4 else ("#E0218A" if stress_level < 7 else "#FF1493")
    
    st.markdown(f"""
    <div class="intensity-box">
        <div class="slider-value" style="color: {stress_color};">{stress_level}/10</div>
        <div style="color: #FFB6D9;">{stress_levels[stress_level]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.user_data['stress_levels'] = stress_level
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Accessibility Section
    st.markdown('<div class="section-header">📍 Substance Accessibility</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    How easy is it to access substances right now?
    </div>
    """, unsafe_allow_html=True)
    
    accessibility = st.slider(
        "Accessibility (0 = No access, 5 = Very easy access)",
        min_value=0,
        max_value=5,
        value=0,
        key="accessibility_slider"
    )
    
    # Display accessibility level
    access_levels = ["No access", "Very difficult", "Difficult", "Moderate", "Easy", "Very easy"]
    access_color = "#FF6EC7" if accessibility < 2 else ("#E0218A" if accessibility < 4 else "#FF1493")
    
    st.markdown(f"""
    <div class="intensity-box">
        <div class="slider-value" style="color: {access_color};">{accessibility}/5</div>
        <div style="color: #FFB6D9;">{access_levels[accessibility]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.user_data['accessibility_or_exposure'] = accessibility
    
    # Craving types (simple multiselect)
    st.markdown('<div class="section-header">📋 Craving Types</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFB6D9; margin-bottom: 1rem; font-size: 0.95em;">
    What types of cravings do you experience?
    </div>
    """, unsafe_allow_html=True)
    
    selected_cravings = st.multiselect(
        "Select craving types:",
        CRAVING_TYPES,
        help="Select all that apply",
        key="cravings_multiselect"
    )
    
    # Handle "None" selection
    if selected_cravings and "None" in selected_cravings:
        selected_cravings = ["None"]
        st.info("'None' selected - other craving types have been cleared.")
    
    if selected_cravings:
        st.session_state.user_data['cravings'] = ', '.join(selected_cravings)
        
        # Show selected cravings horizontally
        if selected_cravings != ["None"]:
            st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="color: #FFB6D9; margin-bottom: 0.5rem;">Selected cravings:</div>
                <div class="pill-container">
            """, unsafe_allow_html=True)
            
            for craving in selected_cravings:
                st.markdown(f'<span class="pill-badge">{craving}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back", use_container_width=True):
            prev_step()
    with col3:
        if st.button("Next →", use_container_width=True):
            if selected_cravings:
                st.markdown(f"""
                <div class="info-note">
                ✨ Thank you for your honesty. Now let's talk about medication.
                </div>
                """, unsafe_allow_html=True)
                next_step()
            else:
                st.markdown("""
                <div class="warning-box">
                💗 Please select at least one craving type.
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# STEP 5: MEDICATION
# =========================================================
elif st.session_state.current_step == 5:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">💊 Medication Information</h3>
        <p style="color: #FFB6D9;">
        Understanding your current medications helps provide better support.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    medication_option = st.selectbox(
        "Are you currently taking any medication?",
        ["", "Yes", "No"],
        key="medication_select"
    )
    
    if medication_option == "Yes":
        medication_name = st.text_input("Please enter the medication name(s):", key="medication_name")
        if medication_name:
            st.session_state.user_data['medication'] = medication_name
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back", use_container_width=True):
                    prev_step()
            with col3:
                if st.button("Next →", use_container_width=True):
                    next_step()
    elif medication_option == "No":
        st.session_state.user_data['medication'] = 'None'
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Next →", use_container_width=True):
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please select an option.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 6: SELF-ESTEEM ASSESSMENT
# =========================================================
elif st.session_state.current_step == 6:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">🌟 Self-Esteem Assessment</h3>
        <p style="color: #FFB6D9;">
        Rate how much you agree with each statement (0-3)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    self_esteem_questions = [
        "I feel good about myself most of the time.",
        "I believe I have value as a person.",
        "I am confident in my abilities.",
        "I feel worthy of love and respect."
    ]
    
    rating_options = ["0 - Strongly disagree", "1 - Disagree", "2 - Agree", "3 - Strongly agree"]
    
    self_esteem_score = 0
    
    for i, question in enumerate(self_esteem_questions):
        st.markdown(f"**{i+1}. {question}**")
        rating_display = st.selectbox(
            f"Select rating:",
            rating_options,
            key=f"self_esteem_select_{i}",
            index=1  # Default to "1 - Disagree"
        )
        
        rating = int(rating_display.split(" - ")[0])
        self_esteem_score += rating
    
    # Score visualization
    max_score = 12
    score_percentage = (self_esteem_score / max_score) * 100
    score_color = "#FF6EC7" if score_percentage < 33 else ("#E0218A" if score_percentage < 66 else "#FF1493")
    
    st.markdown(f"""
    <div class="intensity-box">
        <div style="color: #FFB6D9; margin-bottom: 0.5rem;">Self-Esteem Score</div>
        <div class="slider-value" style="color: {score_color};">{self_esteem_score}/{max_score}</div>
        <div style="color: #999999; font-size: 0.9em; margin-top: 0.5rem;">
        {['Needs attention', 'Room for growth', 'Good', 'Excellent'][min(self_esteem_score // 3, 3)]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.user_data['self_esteem'] = self_esteem_score
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back", use_container_width=True):
            prev_step()
    with col3:
        if st.button("Next →", use_container_width=True):
            next_step()

# =========================================================
# STEP 7: MENTAL HEALTH CONDITIONS (USING MULTISELECT)
# =========================================================
elif st.session_state.current_step == 7:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">🧠 Mental Health Conditions</h3>
        <p style="color: #FFB6D9;">
        Understanding your mental health helps provide appropriate support.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use multiselect for mental health conditions
    selected_conditions = st.multiselect(
        "Select diagnosed mental health conditions:",
        MENTAL_HEALTH_CONDITIONS,
        help="Select all that apply",
        key="mh_multiselect"
    )
    
    # Handle "Other" selection
    if "Other" in selected_conditions:
        other_condition = st.text_input("Please specify the other condition:", key="other_condition_mh")
        if other_condition:
            selected_conditions.remove("Other")
            selected_conditions.append(other_condition)
    
    # Handle "None" selection
    if selected_conditions and "None" in selected_conditions:
        selected_conditions = ["None"]
        st.info("'None' selected - other conditions have been cleared.")
    
    if selected_conditions:
        st.session_state.user_data['mental_health_conditions'] = ', '.join(selected_conditions)
        
        # Show selected conditions horizontally
        if selected_conditions != ["None"]:
            st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="color: #FFB6D9; margin-bottom: 0.5rem;">Selected conditions:</div>
                <div class="pill-container">
            """, unsafe_allow_html=True)
            
            for condition in selected_conditions:
                st.markdown(f'<span class="pill-badge">{condition}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Next →", use_container_width=True):
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please select at least one option.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 8: LIFE STRESSORS (USING MULTISELECT)
# =========================================================
elif st.session_state.current_step == 8:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">🌪️ Life Stressors</h3>
        <p style="color: #FFB6D9;">
        Identifying current stressors helps develop coping strategies.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use multiselect for stressors
    selected_stressors = st.multiselect(
        "Select current life stressors:",
        LIFE_STRESSORS,
        help="Select all that apply",
        key="stressors_multiselect"
    )
    
    # Handle "None" selection
    if selected_stressors and "None" in selected_stressors:
        selected_stressors = ["None"]
        st.info("'None' selected - other stressors have been cleared.")
    
    if selected_stressors:
        st.session_state.user_data['life_stressors'] = ', '.join(selected_stressors)
        
        if selected_stressors != ["None"]:
            st.markdown("""
            <div style="margin-top: 1rem;">
                <div style="color: #FFB6D9; margin-bottom: 0.5rem;">Selected stressors:</div>
                <div class="pill-container">
            """, unsafe_allow_html=True)
            
            for stressor in selected_stressors:
                st.markdown(f'<span class="pill-badge">{stressor}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-note">
        ✨ Thank you for sharing. Recognizing stressors is the first step to managing them.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Next →", use_container_width=True):
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please select at least one option.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 9: SUPPORT SYSTEM (USING MULTISELECT)
# =========================================================
elif st.session_state.current_step == 9:
    show_progress()
    
    st.markdown("""
    <div class="dark-container">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">🤝 Support System</h3>
        <p style="color: #FFB6D9;">
        Your support network plays a crucial role in recovery.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use multiselect for support system
    selected_support = st.multiselect(
        "Select your support system:",
        SUPPORT_OPTIONS,
        help="Select all that apply",
        key="support_multiselect"
    )
    
    # Handle "None" selection
    if selected_support and "None" in selected_support:
        selected_support = ["None"]
        st.info("'None' selected - other support options have been cleared.")
    
    if selected_support:
        st.session_state.user_data['support'] = ', '.join(selected_support)
        
        # Visual display of support system horizontally
        if selected_support != ["None"]:
            st.markdown("""
            <div style="margin-top: 1.5rem;">
                <div style="color: #FF6EC7; font-size: 1.2em; margin-bottom: 1rem; text-align: center;">
                    Your Support Network
                </div>
                <div class="pill-container" style="justify-content: center;">
            """, unsafe_allow_html=True)
            
            for support in selected_support:
                st.markdown(f"""
                <span class="pill-badge" style="background: rgba(224, 33, 138, 0.3); font-size: 1em; padding: 0.8rem 1.2rem;">
                    {support}
                </span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back", use_container_width=True):
                prev_step()
        with col3:
            if st.button("Get Results 🌸", use_container_width=True):
                # Make predictions
                relapse_phase, relapse_prob = predict_relapse_risk(st.session_state.user_data)
                st.session_state.user_data['relapse_phase'] = relapse_phase
                st.session_state.user_data['prob_of_relapse'] = relapse_prob
                
                # Store data
                store_data(st.session_state.user_data)
                next_step()
    else:
        st.markdown("""
        <div class="warning-box">
        💗 Please select your support system.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STEP 10: RESULTS PAGE (FIXED FORMATTING)
# =========================================================
elif st.session_state.current_step == 10:
    user_data = st.session_state.user_data
    
    # Beautiful results header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div style="font-size: 4em; margin-bottom: 1rem; color: #E0218A;">📊</div>
        <h1>Your Assessment Results</h1>
        <p style="color: #FFB6D9; font-size: 1.1em;">
        Personalized analysis for {first_name}
        </p>
    </div>
    """.format(first_name=user_data.get('first_name', '')), unsafe_allow_html=True)
    
    # Main results card
    relapse_phase = user_data.get('relapse_phase', 'medium')
    relapse_prob = user_data.get('prob_of_relapse', 0.5)
    prob_percent = relapse_prob * 100
    
    # Determine status styling
    if relapse_phase == 'low':
        status_class = "status-low"
        status_icon = "✅"
        risk_text = "LOW RISK"
    elif relapse_phase == 'medium':
        status_class = "status-medium"
        status_icon = "⚠️"
        risk_text = "MEDIUM RISK"
    else:
        status_class = "status-high"
        status_icon = "🚨"
        risk_text = "HIGH RISK"
    
    st.markdown(f"""
    <div class="result-card">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3em; margin-bottom: 1rem;">{status_icon}</div>
            <h2 style="margin-bottom: 0.5rem;" class="{status_class}">{risk_text}</h2>
            <p style="color: #FFB6D9;">Predicted Relapse Phase</p>
        </div>
        
        <div style="background: #000000; padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center;">
            <div class="big-number">{prob_percent:.1f}%</div>
            <p style="color: #FFB6D9; margin-top: 0.5rem;">Probability of Relapse</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Factors Section with ACTUAL DATA
    st.markdown("""
    <div class="result-card">
        <h3 style="color: #ffffff; margin-bottom: 1.5rem; border-bottom: 2px solid #E0218A; padding-bottom: 0.5rem;">
            🔑 Key Contributing Factors
        </h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    # Factor 1: Stress
    stress = user_data.get('stress_levels', 5)
    stress_color = "#FF6EC7" if stress < 4 else ("#E0218A" if stress < 7 else "#FF1493")
    
    # Factor 2: Cravings
    cravings = user_data.get('craving_intensity', 5)
    craving_color = "#FF6EC7" if cravings < 4 else ("#E0218A" if cravings < 7 else "#FF1493")
    
    # Factor 3: Support
    support = user_data.get('support', 'None')
    if isinstance(support, str):
        support_list = [s.strip() for s in support.split(',')]
    else:
        support_list = [support] if support else ['None']
    
    support_factor = len(support_list) if 'None' not in support_list else 0
    support_color = "#FF1493" if support_factor == 0 else ("#E0218A" if support_factor < 3 else "#FF6EC7")
    
    # Factor 4: Self-Esteem
    self_esteem = user_data.get('self_esteem', 6)
    esteem_percent = (self_esteem / 12) * 100
    esteem_color = "#FF1493" if esteem_percent < 33 else ("#E0218A" if esteem_percent < 66 else "#FF6EC7")
    
    st.markdown(f"""
        <div style="background: #1a1a1a; padding: 1.2rem; border-radius: 10px; border-left: 3px solid {stress_color};">
            <div style="color: #FFB6D9; font-size: 0.9em; margin-bottom: 0.5rem;">Stress Level</div>
            <div style="color: {stress_color}; font-size: 1.5em; font-weight: 700;">{stress}/10</div>
        </div>
        
        <div style="background: #1a1a1a; padding: 1.2rem; border-radius: 10px; border-left: 3px solid {craving_color};">
            <div style="color: #FFB6D9; font-size: 0.9em; margin-bottom: 0.5rem;">Craving Intensity</div>
            <div style="color: {craving_color}; font-size: 1.5em; font-weight: 700;">{cravings}/10</div>
        </div>
        
        <div style="background: #1a1a1a; padding: 1.2rem; border-radius: 10px; border-left: 3px solid {support_color};">
            <div style="color: #FFB6D9; font-size: 0.9em; margin-bottom: 0.5rem;">Support Sources</div>
            <div style="color: {support_color}; font-size: 1.5em; font-weight: 700;">{support_factor}</div>
        </div>
        
        <div style="background: #1a1a1a; padding: 1.2rem; border-radius: 10px; border-left: 3px solid {esteem_color};">
            <div style="color: #FFB6D9; font-size: 0.9em; margin-bottom: 0.5rem;">Self-Esteem</div>
            <div style="color: {esteem_color}; font-size: 1.5em; font-weight: 700;">{self_esteem}/12</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Personalized Guidance Section
    st.markdown("""
    <div class="result-card">
        <h3 style="color: #ffffff; margin-bottom: 1.5rem; border-bottom: 2px solid #E0218A; padding-bottom: 0.5rem;">
            💝 Personalized Guidance
        </h3>
    """, unsafe_allow_html=True)
    
    if relapse_phase == 'low':
        st.markdown("""
        <div style="background: rgba(255, 110, 199, 0.1); padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: #FF6EC7; margin-bottom: 1rem;">🎉 You're Doing Amazing!</h4>
            <p style="color: #FFB6D9; line-height: 1.6; margin-bottom: 1rem;">
            Your assessment shows you're at a <b>low risk</b> of relapse. This is a testament to your 
            hard work and commitment to recovery. Keep up the excellent progress!
            </p>
            
            <div style="background: rgba(255, 110, 199, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #FF6EC7; font-weight: 600; margin-bottom: 0.5rem;">🌸 Recommended Actions:</p>
                <ul style="color: #FFB6D9; padding-left: 1.2rem;">
                    <li>Continue practicing your healthy coping strategies</li>
                    <li>Maintain regular contact with your support system</li>
                    <li>Celebrate your milestones and achievements</li>
                    <li>Stay mindful of potential triggers as they arise</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif relapse_phase == 'medium':
        st.markdown("""
        <div style="background: rgba(224, 33, 138, 0.1); padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: #E0218A; margin-bottom: 1rem;">⚠️ Increased Awareness Needed</h4>
            <p style="color: #FFB6D9; line-height: 1.6; margin-bottom: 1rem;">
            Your assessment indicates a <b>medium risk</b> of relapse. This is a good time to 
            strengthen your coping strategies and increase your support network contact.
            </p>
            
            <div style="background: rgba(224, 33, 138, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #E0218A; font-weight: 600; margin-bottom: 0.5rem;">🌸 Recommended Actions:</p>
                <ul style="color: #FFB6D9; padding-left: 1.2rem;">
                    <li>Increase contact with your support system this week</li>
                    <li>Practice mindfulness or meditation for 10 minutes daily</li>
                    <li>Avoid known triggers when possible</li>
                    <li>Consider speaking with a therapist or counselor</li>
                    <li>Journal about your feelings and cravings</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:  # high
        st.markdown("""
        <div style="background: rgba(255, 20, 147, 0.1); padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: #FF1493; margin-bottom: 1rem;">🚨 Immediate Action Recommended</h4>
            <p style="color: #FFB6D9; line-height: 1.6; margin-bottom: 1rem;">
            Your assessment shows a <b>high risk</b> of relapse. Please know that this doesn't 
            mean you've failed—it means you need extra support right now.
            </p>
            
            <div style="background: rgba(255, 20, 147, 0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #FF1493; font-weight: 600; margin-bottom: 0.5rem;">🌸 Immediate Actions:</p>
                <ul style="color: #FFB6D9; padding-left: 1.2rem;">
                    <li><b>Contact your support system immediately</b></li>
                    <li>Avoid all situations that could trigger substance use</li>
                    <li>Reach out to a professional or treatment provider</li>
                    <li>Use crisis resources if needed (listed below)</li>
                    <li>Practice deep breathing and grounding techniques</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Emergency resources
        st.markdown("""
        <div class="warning-box" style="margin-top: 1.5rem;">
            <h4 style="color: #FF1493; margin-bottom: 0.5rem;">📞 Emergency Support Resources:</h4>
            <p style="margin: 0.25em 0; color: #FFB6D9;">• <b>National Helpline:</b> 1-800-662-HELP (4357) - 24/7 free, confidential treatment referral</p>
            <p style="margin: 0.25em 0; color: #FFB6D9;">• <b>Crisis Text Line:</b> Text HOME to 741741 - Free 24/7 crisis support</p>
            <p style="margin: 0.25em 0; color: #FFB6D9;">• <b>Emergency:</b> Call 911 or go to the nearest emergency room</p>
            <p style="margin: 0.25em 0; color: #FFB6D9;">• <b>988 Suicide & Crisis Lifeline:</b> Call or text 988</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Final encouragement
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; background: linear-gradient(135deg, rgba(224, 33, 138, 0.1) 0%, rgba(255, 110, 199, 0.1) 100%); 
                border-radius: 15px; border: 1px solid rgba(224, 33, 138, 0.3);">
        <p style="font-size: 1.3em; font-weight: 600; color: #FF6EC7; margin-bottom: 0.5rem;">
        Recovery is a journey of courage, not perfection.
        </p>
        <p style="color: #FFB6D9; max-width: 600px; margin: 0 auto;">
        Every step you take toward self-awareness and healing matters. 
        You've shown incredible strength by completing this assessment.
        </p>
        <p style="font-size: 1.5em; font-weight: 700; color: #FF6EC7; margin-top: 1rem;">
        You've got this! 💝
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📥 Save Results", use_container_width=True):
            st.success("Results have been saved to sophia_dataset.csv")
    
    with col2:
        if st.button("🔄 New Assessment", use_container_width=True):
            reset_app()
    
    with col3:
        if st.button("🏠 Return Home", use_container_width=True):
            reset_app()

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style="text-align: center; color: #666666; font-size: 0.9em; margin-top: 3em; padding-top: 1em; border-top: 1px solid #333333;">
🌸 <b>Sophia</b> is a relapse prevention tool. This is not medical advice. If you're in crisis, please contact a healthcare professional or emergency services.
</div>
""", unsafe_allow_html=True)
