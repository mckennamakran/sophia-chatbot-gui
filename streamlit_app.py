import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import os
import csv
from datetime import datetime
import json

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Sophia | Compassionate Relapse Prevention",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== UPDATED DARK THEME CSS WITH HOT/BARBIE PINK ACCENTS ====================
st.markdown("""
<style>
    /* Professional Dark Theme with Hot/Barbie Pink Accents */
    :root {
        --bg-primary: #0A0E17;
        --bg-secondary: #121826;
        --bg-card: #1A1F2E;
        --bg-input: #2D3448;
        --border: #3A425C;
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --accent-primary: #FF69B4;
        --accent-secondary: #FF1493;
        --accent-light: #FFB6C1;
        --accent-hot: #FF007F;
        --accent-barbie: #FF00A0;
        --accent-neon: #FF00FF;
        --accent-slider: #FF85B3;
        --success: #FF69B4;
        --warning: #FFB6C1;
        --danger: #FF007F;
        --info: #FF00A0;
    }
    
    /* Main App */
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em;
    }
    
    h1 {
        color: var(--accent-barbie) !important;
        font-size: 2.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        color: var(--accent-light) !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-barbie);
    }
    
    h3 {
        color: var(--text-primary) !important;
        font-size: 1.4rem !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    /* Cards */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: var(--accent-barbie);
        box-shadow: 0 8px 32px rgba(255, 0, 160, 0.15);
    }
    
    /* ALL INPUT FIELDS - Pink Border (ALL Inputs) */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea,
    .stMultiSelect > div > div > div {
        border-color: var(--accent-hot) !important;
        border-width: 1px !important;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: var(--bg-input) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    
    /* Input fields on focus - Hot Pink Border */
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div[data-baseweb="select"]:focus-within,
    .stTextArea > div > div > textarea:focus,
    .stMultiSelect > div > div > div:focus-within {
        border-color: var(--accent-hot) !important;
        box-shadow: 0 0 0 1px var(--accent-hot) !important;
    }
    
    /* MultiSelect specific styling */
    .stMultiSelect > div > div > div {
        background: var(--bg-input) !important;
        border-radius: 8px !important;
    }
    
    /* Selectbox specific styling - Remove red background */
    .stSelectbox > div > div > div > div > div {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: var(--text-primary) !important;
        background-color: var(--bg-input) !important;
    }
    
    /* Buttons - Hot Pink */
    .stButton > button {
        background: var(--accent-hot) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--accent-barbie) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 0, 160, 0.3) !important;
    }
    
    /* Sliders - Lighter Pink Track */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--accent-slider), var(--accent-light)) !important;
    }
    
    /* Slider thumb */
    .stSlider > div > div > div > div > div {
        background: var(--accent-hot) !important;
        border-color: var(--accent-hot) !important;
    }
    
    /* Tabs - Hot Pink Active */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-hot) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(255, 0, 127, 0.2);
    }
    
    /* Checkboxes and multiselect - Hot Pink when selected */
    .stCheckbox > div > label > div:first-child {
        background: var(--accent-hot) !important;
        border-color: var(--accent-hot) !important;
    }
    
    /* Radio buttons - Hot Pink (not red) */
    .stRadio > div > label > div:first-child {
        border-color: var(--accent-hot) !important;
    }
    
    .stRadio > div > label > div:first-child > div {
        background: var(--accent-hot) !important;
    }
    
    /* Metrics */
    .stMetric {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid var(--accent-barbie);
    }
    
    /* Progress bars - Hot Pink */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-hot), var(--accent-barbie)) !important;
    }
    
    /* Section Separators */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-barbie), transparent);
        margin: 40px 0;
        width: 100%;
    }
    
    .subsection-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 30px 0;
        width: 100%;
    }
    
    /* Compassionate text styling */
    .compassionate-text {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .therapy-note {
        background: rgba(255, 0, 160, 0.1);
        border-left: 4px solid var(--accent-barbie);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        font-style: italic;
    }
    
    /* Status badges - All in Pink Shades */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin: 4px;
    }
    
    .badge-low { 
        background: rgba(255, 182, 193, 0.2); 
        color: #FFB6C1;
        border: 1px solid #FFB6C1;
    }
    
    .badge-medium { 
        background: rgba(255, 105, 180, 0.2); 
        color: #FF69B4;
        border: 1px solid #FF69B4;
    }
    
    .badge-high { 
        background: rgba(255, 0, 127, 0.2); 
        color: #FF007F;
        border: 1px solid #FF007F;
    }
    
    /* Action items */
    .action-item {
        background: rgba(255, 0, 160, 0.05);
        border: 1px solid rgba(255, 0, 160, 0.2);
        border-radius: 10px;
        padding: 16px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .action-item:hover {
        background: rgba(255, 0, 160, 0.1);
        border-color: var(--accent-barbie);
    }
    
    /* Info boxes */
    .info-note {
        background: rgba(255, 0, 160, 0.1);
        border-left: 4px solid var(--accent-neon);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    /* Form labels */
    .stForm > div > div > label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--accent-barbie) !important;
    }
    
    /* Custom container for triggers */
    .trigger-container {
        background: var(--bg-input);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid var(--border);
    }
    
    /* Welcome message */
    .welcome-message {
        background: linear-gradient(135deg, rgba(255, 0, 160, 0.1), rgba(255, 0, 127, 0.1));
        border: 1px solid var(--accent-barbie);
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
FILE_NAME = 'sophia_dataset.csv'

# ==================== EXACT COPY OF YOUR ORIGINAL DATA STRUCTURES ====================
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
    'Emotional': {
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
    'Mental': {
        'a': 'Cravings',
        'b': 'Obsessive thoughts',
        'c': 'Rationalizing use',
        'd': 'Minimizing consequences',
        'e': 'Negative self-talk',
        'f': 'Hopelessness',
        'g': 'Overconfidence in control'
    },
    'Environmental': {
        'a': 'Being around substances',
        'b': 'Certain places',
        'c': 'Easy access to drugs',
        'd': 'Lack of structure',
        'e': 'Being alone too long',
        'f': 'Parties or social events'
    },
    'Social': {
        'a': 'Peer pressure',
        'b': 'Conflict with others',
        'c': 'Feeling judged',
        'd': 'Relationship problems',
        'e': 'Isolation',
        'f': 'Enabling friends or family'
    }
}

CRAVING_TYPES = {
    'a': 'Physical urge',
    'b': 'Mental obsession',
    'c': 'Emotional craving',
    'd': 'Habit-based craving',
    'e': 'Stress-induced craving',
    'f': 'None'
}

# ==================== COMPASSIONATE MESSAGES ====================
COMPASSIONATE_MESSAGES = {
    'welcome': [
        "I'm Sophia, your compassionate companion on this recovery journey.",
        "Every step you take towards healing is a victory, and I'm here to honor that with you.",
        "Your courage in seeking support is the first sign of your strength.",
        "Today, we'll work together to understand your unique journey and create a path forward."
    ],
    'progress': [
        "Thank you for sharing that with me. It takes real courage to be this honest.",
        "I hear you, and I want you to know that everything you're feeling is valid.",
        "You're doing important work right now, and I'm here to support you through it.",
        "Each piece of information you share helps me understand how to support you better."
    ],
    'completion': [
        "Thank you for trusting me with your story. Your vulnerability is a sign of strength.",
        "You've just taken a powerful step towards understanding yourself better.",
        "I'm honored to walk alongside you in this journey of healing and growth.",
        "Your commitment to this process shows incredible resilience."
    ]
}

# ==================== HUMAN-CENTERED ACTION PLANS ====================
HUMAN_ACTION_PLANS = {
    'low': {
        'title': "Acknowledging Your Strength 🌈",
        'introduction': "Your journey so far shows remarkable resilience. You're in a space of stability, which is a testament to your hard work.",
        'actions': [
            {
                'title': "Celebrate Your Progress",
                'description': "Take a moment each day to acknowledge how far you've come. Write down one small victory from your recovery journey."
            },
            {
                'title': "Deepen Your Self-Connection",
                'description': "Spend 10 minutes each morning in quiet reflection. Notice what you're feeling without judgment—this builds emotional awareness."
            },
            {
                'title': "Nurture Your Support System",
                'description': "Reach out to someone who supports you, not because you need help, but to strengthen that connection. Share something positive."
            },
            {
                'title': "Explore New Growth Paths",
                'description': "Consider activities that bring you joy and meaning outside of recovery. What did you love before addiction that you might rediscover?"
            },
            {
                'title': "Practice Gratitude for Your Body",
                'description': "Your body has carried you through this journey. Do one gentle, loving thing for your physical self today."
            }
        ],
        'closing': "Remember: Recovery isn't about perfection—it's about showing up for yourself with compassion, even on the good days."
    },
    'medium': {
        'title': "Honoring Your Awareness 🍃",
        'description': "You're noticing some vulnerability, and that's actually a sign of wisdom. Let's work with what you're feeling.",
        'actions': [
            {
                'title': "Create a Gentle Morning Ritual",
                'description': "Start each day with 5 minutes of deep breathing and one kind statement to yourself. This sets a compassionate tone."
            },
            {
                'title': "Identify Your 'Tender Spots'",
                'description': "Without judgment, notice which situations or feelings feel most challenging right now. Just naming them reduces their power."
            },
            {
                'title': "Reach Out Before You Need To",
                'description': "Contact your support person today, not in crisis, but in connection. Share how you're really doing."
            },
            {
                'title': "Create a 'Comfort Kit'",
                'description': "Gather items that soothe you—a favorite blanket, calming music, photos of loved ones, comforting scents."
            },
            {
                'title': "Practice the 'Pause & Breathe' Technique",
                'description': "When you feel unsettled, pause for three deep breaths. Imagine you're breathing in peace, breathing out tension."
            },
            {
                'title': "Journal Without Editing",
                'description': "Write for 10 minutes without worrying about grammar or sense. Let your feelings flow onto the page without censorship."
            }
        ],
        'closing': "This is a moment of learning, not failure. Each time you recognize a trigger, you're building your recovery muscles."
    },
    'high': {
        'title': "You Are Not Alone 🤝",
        'description': "Right now feels intense, and that's completely understandable. Let's create some immediate comfort and safety.",
        'actions': [
            {
                'title': "Immediate Grounding",
                'description': "Find one thing you can see, one you can hear, one you can feel. Name them quietly. You're here, you're safe in this moment."
            },
            {
                'title': "Reach for Connection",
                'description': "Call or text your support person right now. You don't need to have the right words—just say 'I'm having a hard moment.'"
            },
            {
                'title': "Create a Safe Space",
                'description': "Go to a room that feels comforting. Wrap yourself in a blanket. This is your protective cocoon for now."
            },
            {
                'title': "Speak to Your Younger Self",
                'description': "What would you say to a child who was feeling this way? Offer yourself that same tenderness and reassurance."
            },
            {
                'title': "Use Your Emergency Contacts",
                'description': "Don't hesitate to reach out to your therapist, support group, or crisis line. Asking for help is an act of courage."
            },
            {
                'title': "One Gentle Movement",
                'description': "Stand up and gently stretch your arms toward the sky, then fold forward. Connect with your body's presence."
            },
            {
                'title': "The 'Just For Now' Promise",
                'description': "Tell yourself: 'Just for the next hour, I will stay safe. Just for this hour, I will breathe.' Break it down to manageable moments."
            }
        ],
        'closing': "This intensity will pass. You have survived every hard moment before this one. I believe in your resilience, even when you might not."
    }
}

# ==================== EXACT COPY OF YOUR ORIGINAL ML FUNCTIONS ====================
@st.cache_resource
def load_and_train_models():
    """EXACT COPY: Load and train ML models from your code"""
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        try:
            df = pd.read_csv(FILE_NAME)
            
            if len(df) < 2:
                return None, None, None, None, None
            
            features = ['age', 'gender', 'addiction_type', 'triggers', 'cravings', 'craving_intensity',
                       'accessibility_or_exposure', 'medication', 'stress_levels', 'self_esteem',
                       'mental_health_conditions', 'life_stressors', 'support']
            
            target_class = 'relapse_phase'
            target_reg = 'prob_of_relapse'
            
            if not all(col in df.columns for col in features + [target_class, target_reg]):
                return None, None, None, None, None
            
            X = df[features]
            y_class = df[target_class]
            y_reg = df[target_reg]
            
            categorical_cols = ['gender', 'addiction_type', 'triggers', 'cravings',
                              'medication', 'mental_health_conditions', 'life_stressors', 'support']
            
            encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
            encoder.fit(X[categorical_cols])
            
            numerical_cols = ['age', 'accessibility_or_exposure', 'craving_intensity', 
                             'stress_levels', 'self_esteem']
            
            X_encoded = encoder.transform(X[categorical_cols])
            X_final = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(categorical_cols))
            X_final[numerical_cols] = X[numerical_cols].reset_index(drop=True)
            
            clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            clf_model.fit(X_final, y_class)
            
            reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
            reg_model.fit(X_final, y_reg)
            
            return clf_model, reg_model, encoder, categorical_cols, numerical_cols
            
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            return None, None, None, None, None
    return None, None, None, None, None

def prepare_user_data(user_data, encoder, categorical_cols, numerical_cols):
    """EXACT COPY: Prepare user data for model prediction from your code"""
    df_user = pd.DataFrame([user_data])
    cat_encoded = encoder.transform(df_user[categorical_cols])
    df_encoded = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(categorical_cols))
    df_encoded[numerical_cols] = df_user[numerical_cols].reset_index(drop=True)
    return df_encoded

def classify_relapse(user_data, clf_model, encoder, categorical_cols, numerical_cols):
    """EXACT COPY: Predict relapse phase from your code"""
    if not clf_model or not encoder:
        return "Unknown"
    df_input = prepare_user_data(user_data, encoder, categorical_cols, numerical_cols)
    return clf_model.predict(df_input)[0]

def predict_relapse_probability(user_data, reg_model, encoder, categorical_cols, numerical_cols):
    """EXACT COPY: Predict probability of relapse from your code"""
    if not reg_model or not encoder:
        return 0.5
    df_input = prepare_user_data(user_data, encoder, categorical_cols, numerical_cols)
    return round(float(reg_model.predict(df_input)[0]), 2)

def store_data(user_data):
    """EXACT COPY: Store user data to CSV from your code"""
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
    
    with open(FILE_NAME, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writerow(user_data)



# ==================== COMPASSIONATE UI COMPONENTS ====================
def render_welcome():
    with st.container():
        st.markdown("""
        <div class="welcome-message">
            <h1>Welcome to Sophia 🌸</h1>
            <p class="compassionate-text">
                I'm here to walk beside you on your recovery journey with compassion, understanding, 
                and evidence-based support. This isn't just an assessment—it's a conversation between 
                two humans, with AI as our tool for deeper understanding.
            </p>
            <p class="compassionate-text">
                Take your time with each section. There's no rush. Your comfort and readiness are what 
                matter most.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_section_divider(title):
    """Create a section with title only (no centered pink separator line)"""
    st.markdown(
        f"""
        <div class="section-divider-container">
            <h2>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_subsection_divider():
    """Create a subsection divider (no centered pink separator line)"""
    st.markdown(
        """
        <div class="subsection-divider-container">
            <hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;">
        </div>
        """,
        unsafe_allow_html=True
    )


def render_compassionate_note(text):
    """Render a compassionate note INSIDE its div"""
    st.markdown(
        f"""
        <div class="therapy-note">
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_basic_info():
    """Basic information section with compassionate approach"""
    st.markdown("""
    <div class="therapy-note">
        <p>Let's start gently. Knowing a little about you helps me understand your unique journey. 
        Every story is different, and I want to honor yours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", key="first_name", help="What name do you prefer to be called?")
        age = st.number_input("Age", min_value=1, max_value=120, value=25, 
                            help="Your age helps me understand your life stage context")
    
    with col2:
        surname = st.text_input("Last Name", key="surname")
        gender = st.selectbox("Gender Identity", 
                            ['Select your gender identity...', 
                             'Male', 
                             'Female', 
                             'Non-binary',
                             'Transgender',
                             'Genderqueer',
                             'Prefer not to say',
                             'Other (please specify)'], 
                            key="gender")
    
    if gender == 'Other (please specify)':
        other_gender = st.text_input("Please share your gender identity:", key="other_gender")
        if other_gender:
            gender = other_gender
    
    return {
        'first_name': first_name,
        'surname': surname,
        'age': age,
        'gender': gender if gender != 'Select your gender identity...' else ''
    }

def render_addiction_info():
    """Simplest working version - no fancy logic"""
    
    # Intro note
    st.markdown("""
    <div class="therapy-note">
        <p>Understanding your relationship with substances helps me tailor support specifically for you. 
        There's no judgment here—only understanding.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;">', unsafe_allow_html=True)
    st.markdown('<h4>What type of substance are you working with?</h4>', unsafe_allow_html=True)

    # Columns for dropdowns
    col1, col2 = st.columns(2)
    
    with col1:
        # Create group options with display names
        group_display_options = ["-- Select Group --"]
        group_mapping = {}  # Map display names to keys
        
        for key, value in ADDICTION_GROUPS.items():
            display_name = f"{key}. {value['group_name']}"
            group_display_options.append(display_name)
            group_mapping[display_name] = key
        
        selected_group_display = st.selectbox(
            "Substance Group",
            group_display_options,
            key="group_select_2"
        )
    
    # Always show second dropdown, but control its options
    with col2:
        if selected_group_display != "-- Select Group --":
            group_key = group_mapping[selected_group_display]
            group_data = ADDICTION_GROUPS[group_key]
            
            # Create drug options
            drug_display_options = ["-- Select Substance --"]
            drug_mapping = {}
            
            for d_key, d_name in group_data['drugs'].items():
                display_name = f"{d_key}. {d_name}"
                drug_display_options.append(display_name)
                drug_mapping[display_name] = (d_key, d_name)
            
            selected_drug_display = st.selectbox(
                "Specific Substance",
                drug_display_options,
                key="drug_select_2"
            )
            
            if selected_drug_display != "-- Select Substance --":
                drug_key, drug_name = drug_mapping[selected_drug_display]
                group_name = group_data['group_name']
                addiction_type = f"{group_name} -> {drug_name}"
                
                st.markdown("""
                <div class="info-note" style="margin-top: 20px;">
                ✨ Thank you for sharing. We'll use this information to personalize your support plan.
                </div>
                """, unsafe_allow_html=True)
                
                return addiction_type
            else:
                st.markdown("""
                <div class="info-note" style="margin-top: 20px; border-left-color: #FF69B4;">
                💗 Please select a specific substance.
                </div>
                """, unsafe_allow_html=True)
                return ""
        else:
            # Show disabled dropdown when no group selected
            st.selectbox(
                "Specific Substance",
                ["Select a group first"],
                key="drug_select_disabled",
                disabled=True
            )
            st.markdown("""
            <div class="info-note" style="margin-top: 20px; border-left-color: #FFB6C1;">
            💗 Please select a substance group first.
            </div>
            """, unsafe_allow_html=True)
            return ""
    
    return ""




def render_triggers_section():
    """Triggers section - clean and compassionate"""
    st.markdown("""
    <div class="therapy-note">
        <p>Triggers are normal—they're signals from our experiences and emotions. 
        Identifying them isn't about blame, but about understanding your patterns with kindness.</p>
    </div>
    """, unsafe_allow_html=True)
    
    all_selected_triggers = []
    
    for category, trigger_dict in TRIGGERS.items():
        st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
        st.markdown(f'<h4>{category} Triggers</h4>', unsafe_allow_html=True)
        
        # Clean trigger display without letters
        trigger_options = list(trigger_dict.values())
        
        # Multiselect for triggers
        selected_triggers = st.multiselect(
            f"Which {category.lower()} experiences tend to challenge you?",
            trigger_options,
            key=f"triggers_{category}",
            help="Select all that feel relevant to your experience"
        )
        
        all_selected_triggers.extend(selected_triggers)
    
    return ', '.join(all_selected_triggers) if all_selected_triggers else 'None identified'

def render_cravings_section():
    """Cravings section with compassionate language"""
    st.markdown("""
    <div class="therapy-note">
        <p>Cravings are messages from our body and mind—they don't define who we are. 
        Let's explore them with curiosity rather than criticism.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    # Clean craving options without letters
    craving_options = list(CRAVING_TYPES.values())
    
    # Multiselect for cravings
    selected_cravings = st.multiselect(
        "What kinds of cravings do you experience?",
        craving_options,
        key="cravings",
        help="Select the types that resonate with your experience"
    )
    
    craving_str = ', '.join(selected_cravings) if selected_cravings else 'None currently'
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    # Intensity with compassionate framing
    st.markdown('<h4>How intense are these feelings for you right now?</h4>', unsafe_allow_html=True)
    intensity = st.slider(
        "On a scale where 0 is barely noticeable and 10 feels overwhelming",
        min_value=0,
        max_value=10,
        value=5,
        key="craving_intensity",
        help="There's no right or wrong answer—just what's true for you now"
    )
    
    return craving_str, intensity

def render_accessibility_section():
    """Accessibility section"""
    st.markdown("""
    <div class="therapy-note">
        <p>Understanding your environment helps us create practical strategies. 
        This isn't about willpower—it's about creating supportive conditions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    accessibility = st.slider(
        "How accessible are substances in your current environment?",
        min_value=0,
        max_value=5,
        value=2,
        key="accessibility",
        help="0 = No access, 5 = Very easy access"
    )
    
    return accessibility

def render_medication_section():
    """Medication section with yes/no and conditional input field"""
    st.markdown("""
    <div class="therapy-note">
        <p>Medications can be important tools in healing. Let's understand what you're working with.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    # Yes/No for medication
    medication_option = st.radio(
        "Are you currently taking any medications?",
        ['No', 'Yes'],
        key="medication_option",
        horizontal=True
    )
    
    medication_details = ''
    
    if medication_option == 'Yes':
        medication_details = st.text_area(
            "Please list the medications you're taking:",
            placeholder="e.g., Antidepressants, Anti-anxiety medication, Pain relievers...",
            key="medication_details",
            help="This helps me understand your full picture of care"
        )
        if medication_details:
            medication = medication_details
        else:
            medication = 'Yes (unspecified)'
    else:
        medication = 'No'
    
    return medication

def render_stress_section():
    """Stress levels with compassionate framing"""
    st.markdown("""
    <div class="therapy-note">
        <p>Stress affects all of us differently. Let's check in with how you're feeling right now.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    stress = st.slider(
        "How would you describe your current stress level?",
        min_value=0,
        max_value=10,
        value=5,
        key="stress_levels",
        help="0 = Completely calm, 10 = Overwhelming stress"
    )
    
    return stress

def render_self_esteem_section():
    """Self-esteem with compassionate questions"""
    st.markdown("""
    <div class="therapy-note">
        <p>Our relationship with ourselves is at the heart of healing. 
        Let's explore this with gentle curiosity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    questions = [
        "I feel good about myself most of the time.",
        "I believe I have value as a person.",
        "I am confident in my abilities.",
        "I feel worthy of love and respect."
    ]
    
    total_score = 0
    for i, question in enumerate(questions):
        st.markdown(f'<strong>{question}</strong>', unsafe_allow_html=True)
        score = st.radio(
            "",
            options=["Strongly disagree", "Disagree", "Agree", "Strongly agree"],
            index=2,
            key=f"self_esteem_{i}",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Convert to numeric
        if score == "Strongly disagree":
            total_score += 0
        elif score == "Disagree":
            total_score += 1
        elif score == "Agree":
            total_score += 2
        else:  # Strongly agree
            total_score += 3
        
        if i < len(questions) - 1:
            st.markdown("---")
    
    return total_score

def render_mental_health_section():
    """Mental health with compassionate framing"""
    st.markdown("""
    <div class="therapy-note">
        <p>Mental health is part of our whole health. Understanding your experiences helps me support you better.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4>Mental Health History</h4>', unsafe_allow_html=True)
        mental_health_options = [
            'Depression',
            'Anxiety',
            'PTSD',
            'Bipolar disorder',
            'ADHD',
            'Personality Disorder',
            'Other',
            'None diagnosed'
        ]
        
        selected_conditions = st.multiselect(
            "Have you been diagnosed with any mental health conditions?",
            mental_health_options,
            key="mental_health"
        )
        
        if 'Other' in selected_conditions:
            other_condition = st.text_input("Please share:", key="other_mental")
            if other_condition:
                selected_conditions.remove('Other')
                selected_conditions.append(other_condition)
    
    with col2:
        st.markdown('<h4>Current Life Challenges</h4>', unsafe_allow_html=True)
        stressor_options = [
            'Financial stress',
            'Work or school pressure',
            'Relationship difficulties',
            'Health concerns',
            'Legal situations',
            'Recent loss or grief',
            'None significant currently'
        ]
        
        selected_stressors = st.multiselect(
            "What challenges are you facing right now?",
            stressor_options,
            key="life_stressors"
        )
    
    mental_conditions = ', '.join(selected_conditions) if selected_conditions else 'None reported'
    life_stressors = ', '.join(selected_stressors) if selected_stressors else 'None significant'
    
    return mental_conditions, life_stressors

def render_support_system():
    """Support system with compassionate framing"""
    st.markdown("""
    <div class="therapy-note">
        <p>Connection is healing. Who or what supports you in this journey?</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-divider-container"><hr style="border: 0; height: 1px; background: #3A425C; margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    support_options = [
        'Family',
        'Friends',
        'Support group (AA/NA/etc.)',
        'Therapist or counselor',
        'Partner or spouse',
        'Online community',
        'Medical team',
        'Building my support system'
    ]
    
    support = st.selectbox(
        "Who is part of your support network?",
        ['Select your primary support...'] + support_options,
        key="support"
    )
    
    return support if support != 'Select your primary support...' else 'Building support system'

# ==================== MAIN APPLICATION ====================
# ... (keep all the imports, constants, and functions above exactly as they are) ...

# ==================== MAIN APPLICATION ====================
def main():
    # Initialize session state
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Load ML models
    with st.spinner("Preparing your personalized support system..."):
        clf_model, reg_model, encoder, categorical_cols, numerical_cols = load_and_train_models()
    
    # Sidebar with compassionate tone
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/heart-health.png", width=80)
        st.markdown("## Sophia 🌸")
        st.markdown("### Your Compassionate Recovery Companion")
        st.markdown("---")
        
        st.markdown("""
        <div class="card">
            <h4>🌟 How This Works</h4>
            <p>This is your safe space for:</p>
            <ul>
                <li><strong>Honest self-reflection</strong></li>
                <li><strong>Personalized insights</strong></li>
                <li><strong>Compassionate guidance</strong></li>
                <li><strong>AI-powered support</strong></li>
            </ul>
            <p>All responses are confidential and secure.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>🚨 Immediate Support</h4>
            <div class="info-note">
                <p><strong>You are not alone. Help is available:</strong></p>
                <p>📞 <strong>SAMHSA</strong>: 1-800-662-HELP (4357)</p>
                <p>💬 <strong>Crisis Text Line</strong>: Text HOME to 741741</p>
                <p>🌐 <strong>Online support</strong>: Available 24/7</p>
                <p><em>Reaching out is an act of courage.</em></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Start Fresh", type="primary"):
            st.session_state.assessment_complete = False
            st.session_state.user_data = {}
            st.rerun()
    
    # Main content
    render_welcome()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🕊️ Assessment", "📖 Your Insights", "🌱 Your Journey"])
    
    with tab1:
        if not st.session_state.assessment_complete:
            st.markdown("""
            <div class="card">
                <h3>Let's Begin Our Conversation</h3>
                <p class="compassionate-text">
                    I'll guide you through some questions about your experiences, feelings, and current situation. 
                    There are no right or wrong answers—only your truth.
                </p>
                <p class="compassionate-text">
                    Take this at your own pace. You can pause anytime, and all your responses are saved privately.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # =============== CRITICAL FIX ===============
            # Section 1: Getting to Know You - OUTSIDE the form
            render_section_divider("Getting to Know You")
            basic_info = render_basic_info()
            
            # Section 2: Understanding Your Experience - OUTSIDE the form
            render_section_divider("Understanding Your Experience")
            addiction_type = render_addiction_info()
            
            # =============== NOW START THE FORM ===============
            # Assessment form (rest of the sections)
            with st.form("sophia_assessment"):
                user_data = {}
                
                # Add the basic info and addiction type that we collected OUTSIDE the form
                user_data.update(basic_info)
                user_data['addiction_type'] = addiction_type
                
                # Progress note
                if user_data.get('first_name'):
                    render_compassionate_note(f"Thank you for sharing that, {user_data['first_name']}. Let's continue with care.")
                
                if addiction_type:
                    render_compassionate_note("Thank you for trusting me with this information. This helps me understand your journey better.")
                
                # Section 3: Emotional Landscape
                render_section_divider("Your Emotional Landscape")
                triggers = render_triggers_section()
                user_data['triggers'] = triggers
                
                cravings, craving_intensity = render_cravings_section()
                user_data['cravings'] = cravings
                user_data['craving_intensity'] = craving_intensity
                
                render_compassionate_note("Noticing these patterns is powerful work. You're building important self-awareness.")
                
                # Section 4: Current Environment
                render_section_divider("Your Current Environment")
                accessibility = render_accessibility_section()
                user_data['accessibility_or_exposure'] = accessibility
                
                render_compassionate_note("Understanding your environment helps us create practical support strategies.")
                
                # Section 5: Health & Wellness
                render_section_divider("Health & Wellness")
                
                col1, col2 = st.columns(2)
                with col1:
                    medication = render_medication_section()
                    user_data['medication'] = medication
                
                with col2:
                    stress = render_stress_section()
                    user_data['stress_levels'] = stress
                
                render_compassionate_note("Your health journey is unique, and every piece matters.")
                
                # Section 6: Self & Identity
                render_section_divider("Self & Identity")
                self_esteem = render_self_esteem_section()
                user_data['self_esteem'] = self_esteem
                
                render_compassionate_note("Your relationship with yourself is at the heart of healing. Thank you for exploring this.")
                
                # Section 7: Mental Health & Challenges
                render_section_divider("Mental Health & Current Challenges")
                mental_health, life_stressors = render_mental_health_section()
                user_data['mental_health_conditions'] = mental_health
                user_data['life_stressors'] = life_stressors
                
                # Section 8: Support & Connection
                render_section_divider("Support & Connection")
                support = render_support_system()
                user_data['support'] = support
                
                render_compassionate_note("Connection is healing. Thank you for sharing about your support network.")
                
                # Submit button
                submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
                with submit_col2:
                    submitted = st.form_submit_button(
                        "🌸 Generate Your Personalized Insights",
                        type="primary",
                        use_container_width=True
                    )
                
                if submitted:
                    # Validate
                    required_fields = [
                        (user_data['first_name'], "First name"),
                        (user_data['surname'], "Last name"),
                        (user_data['gender'], "Gender identity"),
                        (user_data['addiction_type'], "Addiction information"),
                        (user_data['support'], "Support system")
                    ]
                    
                    missing_fields = [name for value, name in required_fields if not value]
                    
                    if missing_fields:
                        st.error(f"Please complete: {', '.join(missing_fields)}")
                    else:
                        # Make predictions
                        with st.spinner("Reflecting on your journey with compassion..."):
                            # Predict relapse phase
                            relapse_phase = classify_relapse(
                                user_data, clf_model, encoder, categorical_cols, numerical_cols
                            )
                            
                            # Predict relapse probability
                            relapse_prob = predict_relapse_probability(
                                user_data, reg_model, encoder, categorical_cols, numerical_cols
                            )
                            
                            # Add predictions
                            user_data['relapse_phase'] = relapse_phase
                            user_data['prob_of_relapse'] = relapse_prob
                            
                            # Store data
                            try:
                                store_data(user_data)
                            except Exception as e:
                                st.warning(f"Note: Could not save to local file. {e}")
                            
                            # Update session state
                            st.session_state.user_data = user_data
                            st.session_state.assessment_complete = True
                            
                            st.success("🌸 Thank you for sharing your journey. Your insights are ready.")
                            st.balloons()
                            st.rerun()
        
        else:
            # Show completion message if assessment is already complete
            st.markdown("""
            <div class="therapy-note">
                <h3>🌸 Assessment Complete</h3>
                <p>Your assessment has been completed. You can view your personalized insights in the "Your Insights" tab, 
                or track your journey in the "Your Journey" tab.</p>
                <p>If you'd like to start a new assessment, click "Start Fresh" in the sidebar.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ... (keep the rest of the tab2 and tab3 code exactly as it is) ...

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
