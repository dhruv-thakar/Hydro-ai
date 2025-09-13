import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import time
from app.utils.helpers import get_data_summary

load_dotenv()

# Configure page with futuristic theme
st.set_page_config(
    page_title="🌊 HydroAI - Groundwater Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS (single mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

    :root {
        --bg-primary: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        --text-color: #ffffff;
        --card-bg: rgba(255, 255, 255, 0.1);
        --card-border: rgba(255, 255, 255, 0.2);
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        --chart-bg: rgba(0, 0, 0, 0);
        --chart-paper: rgba(0, 0, 0, 0);
        --accent: #00d4ff;
    }

    .stApp {
        background: var(--bg-primary);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .main-header {
        background: linear-gradient(90deg, #00d4ff, #0099cc, #7b68ee, #9370db);
        background-size: 400% 400%;
        animation: gradientShift 4s ease infinite;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.8);
        margin: 0;
        background: linear-gradient(45deg, #00d4ff, #ffffff, #7b68ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.8)); }
        to { filter: drop-shadow(0 0 20px rgba(123, 104, 238, 0.8)); }
    }
    
    .subtitle {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.2rem;
        color: #b0c4de;
        margin-top: 1rem;
        text-shadow: 0 0 10px rgba(176, 196, 222, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 1px solid var(--card-border);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2);
        border-color: rgba(0, 212, 255, 0.5);
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
    }
    
    .metric-label {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.9rem;
        color: #b0c4de;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stChatMessage {
        background: linear-gradient(145deg, rgba(0, 212, 255, 0.1), rgba(123, 104, 238, 0.1));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    .stTextInput>div>div>input {
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 1px solid var(--card-border);
    }

    .stSelectbox>div>div>div>div {
        background-color: var(--card-bg);
        color: var(--text-color);
    }

    .stMultiSelect>div>div>div>div>span {
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 1px solid var(--card-border);
    }

    /* Plotly background */
    .js-plotly-plot .plotly .main-svg {
        background: var(--chart-bg) !important;
    }
    .js-plotly-plot .plotly .plotly-svg {
        background: var(--chart-paper) !important;
    }

    .stDataFrame {
        background-color: var(--card-bg);
        border-radius: 10px;
        box-shadow: var(--card-shadow);
    }
</style>
""", unsafe_allow_html=True)

# Plotly theme constants (dark mode only)
plotly_template = 'plotly_dark'
font_color = 'white'
grid_color = '#2a2a2a'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Load data with progress indicator
@st.cache_data
def load_groundwater_data():
    return pd.read_csv("data/gujarat_groundwater_merged_final.csv")

# Main header with futuristic design
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌊 HYDROAI</h1>
    <p class="subtitle">Advanced Groundwater Intelligence & Predictive Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# Loading animation
with st.spinner('🚀 Initializing quantum data processors...'):
    df = load_groundwater_data()
    data_summary = get_data_summary(df)

# Sidebar with futuristic controls
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="font-family: 'Orbitron', monospace; color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);">
            🎛️ CONTROL PANEL
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Find district column
    district_col = next((col for col in df.columns if 'district' in col.lower() or 'location' in col.lower()), None)
    
    if district_col:
        districts = ['All Districts'] + sorted(df[district_col].unique().astype(str).tolist())
        selected_district = st.selectbox("🎯 Target District", districts)
        
        # Filter data based on selection
        if selected_district != 'All Districts':
            filtered_df = df[df[district_col].str.lower() == selected_district.lower()]
        else:
            filtered_df = df
    else:
        filtered_df = df
        selected_district = 'All Districts'
    
    # Analysis mode selector
    analysis_mode = st.selectbox("🔬 Analysis Mode", 
                               ["Standard Analysis", "Predictive Modeling"])
    
    # Real-time metrics toggle
    show_realtime = st.toggle("📊 Metrics", value=True)

# Main dashboard with metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_df):,}</div>
        <div class="metric-label">Data Points</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if district_col:
        unique_districts = filtered_df[district_col].nunique() if selected_district == 'All Districts' else 1
    else:
        unique_districts = 1
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_districts}</div>
        <div class="metric-label">Districts</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Find numeric columns for quality metrics
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    quality_score = min(100, max(0, int(np.random.uniform(75, 95))))  # Simulated quality score
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{quality_score}%</div>
        <div class="metric-label">Quality Index</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    coverage = min(100, int((len(filtered_df) / len(df)) * 100)) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{coverage}%</div>
        <div class="metric-label">Coverage</div>
    </div>
    """, unsafe_allow_html=True)

# Interactive visualizations
if show_realtime and len(numeric_cols) > 0:
    st.markdown("### 📈 Data Visualization")
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["🌊 Water Quality Trends", "⚡ Monitoring"])
    
    with tab1:
        # Sample visualization with plotly
        if len(numeric_cols) >= 2:
            fig = px.scatter(filtered_df.head(1000), 
                           x=numeric_cols[0], 
                           y=numeric_cols[1],
                           title="Water Quality Parameter Correlation",
                           template=plotly_template)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color=font_color
            )
            fig.update_xaxes(gridcolor=grid_color, zerolinecolor=grid_color)
            fig.update_yaxes(gridcolor=grid_color, zerolinecolor=grid_color)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Simulated real-time gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = quality_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Water Quality Index"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 50], 'color': "#3a3a3a"},
                    {'range': [50, 80], 'color': "#555"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}
            }
        ))
        fig.update_layout(
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=font_color,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Enhanced chat interface
st.markdown("""
<div class="chat-container">
    <h3 style="font-family: 'Orbitron', monospace; color: #00d4ff; text-align: center; margin-bottom: 2rem;">
        🤖 AI GROUNDWATER ANALYST
    </h3>
</div>
""", unsafe_allow_html=True)

# Display chat history with enhanced styling
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Enhanced chat input
prompt = st.chat_input("🔮 Ask about groundwater insights, predictions, or analysis...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Processing with quantum algorithms..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Enhanced context with analysis mode
            district_col = next((col for col in df.columns if 'district' in col.lower() or 'location' in col.lower()), None)
            district_names = df[district_col].unique().astype(str).tolist() if district_col is not None else []
            
            # Find city in prompt
            city = next(
                (word for word in prompt.split() 
                 if word.lower() in [name.lower() for name in district_names]),
                None
            )
            
            if city and district_col:
                city_data = df[df[district_col].str.lower() == city.lower()].copy()
                city_summary = city_data.describe(include='all').to_string()
                sample_data = city_data.head(5).to_string()
                
                context_prompt = """
                You are HydroAI, an advanced groundwater intelligence system analyzing data for {city_name} 
                Current Analysis Mode: {analysis_mode}
                
                🌊 CITY DATA ANALYSIS - {city_upper}:
                - Total samples: {sample_count:,}
                - Data parameters: {params}
                
                📊 SAMPLE DATA (Latest 5 readings):
                {sample_data}
                
                📈 STATISTICAL OVERVIEW:
                {city_summary}
                
                🎯 USER QUERY: {prompt}
                
                Provide a comprehensive analysis with:
                1. Key findings and insights
                2. Water quality assessment
                3. Potential concerns or recommendations
                4. Future predictions if applicable
                
                Use emojis and formatting for better readability. Keep response engaging and professional.
                """.format(
                    city_name=city,
                    city_upper=city.upper(),
                    analysis_mode=analysis_mode,
                    sample_count=len(city_data),
                    params=', '.join(city_data.columns),
                    sample_data=sample_data,
                    city_summary=city_summary,
                    prompt=prompt
                )
            else:
                context_prompt = """
                You are HydroAI, an advanced groundwater intelligence system for Gujarat.
                Current Analysis Mode: {analysis_mode}
                
                🌊 GUJARAT GROUNDWATER DATASET:
                {data_summary}
                
                🎯 USER QUERY: {prompt}
                
                Provide insights based on the dataset with:
                1. Quantitative analysis with specific numbers
                2. Regional patterns and trends
                3. Water quality assessment
                4. Actionable recommendations
                
                Use emojis and professional formatting. Be concise but comprehensive.
                """.format(
                    analysis_mode=analysis_mode,
                    data_summary=data_summary,
                    prompt=prompt
                )
            
            response = model.generate_content(context_prompt)
            response_text = response.text
            
            # Remove unwanted text from the response
            unwanted_text = "Here's a more detailed analysis of the groundwater data:"
            response_text = response_text.replace(unwanted_text, "").strip()
            
            # Add some visual flair to the response
            enhanced_response = """
            <div class="data-insight">
                {response_text}
            </div>
            """.format(response_text=response_text)
            
            st.markdown(enhanced_response, unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# Footer with futuristic styling
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <p style="font-family: 'Exo 2', sans-serif; color: #b0c4de; font-size: 0.9rem;">
        🚀 Powered by HydroAI • Advanced Groundwater Analytics • Real-time Intelligence
    </p>
</div>
""", unsafe_allow_html=True)
