

import sys
import importlib
importlib.import_module('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Page configuration for professional presentation
st.set_page_config(
    page_title="🧠 AI Mental Wellbeing Crew",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in .env file")
    st.markdown("""
    **Please add the following to your .env file:**
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    """)
    st.stop()

# Custom CSS for beautiful presentation
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .status-working {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .status-complete {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .stExpander > div:first-child {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .demo-banner {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'crew_results' not in st.session_state:
    st.session_state.crew_results = None
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'assessment': 'pending',
        'action': 'pending',
        'followup': 'pending'
    }

# Demo banner for auditorium presentation
st.markdown("""
<div class="demo-banner">
    🎭 LIVE DEMO: AI-Powered Mental Wellbeing Crew - CrewAI Multi-Agent System
</div>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧠 AI Mental Wellbeing Crew</h1>
    <p>Advanced Multi-Agent System for Personalized Mental Health Support</p>
    <p><em>Powered by CrewAI • Designed for Scale • Built with Compassion</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    
    st.markdown("### 📊 Agent Status Dashboard")
    
    # Status indicators
    status_colors = {
        'pending': '⏳',
        'working': '🔄',
        'complete': '✅'
    }
    
    for agent, status in st.session_state.agent_status.items():
        st.markdown(f"**{agent.title()} Agent:** {status_colors[status]} {status.title()}")
    
    st.markdown("---")
    
    st.markdown("""
    ### ⚠️ Professional Disclaimer
    
    This AI system provides supportive guidance but does not replace professional mental health care.
    
    **Crisis Resources:**
    - 🆘 Crisis Hotline: 988
    - 🚨 Emergency: 911
    - 💬 Crisis Text Line: Text HOME to 741741
    
    Seek immediate professional help for severe distress.
    """)

# Agent information cards
st.markdown("### 🤖 Meet Your AI Mental Wellbeing Crew")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Assessment Specialist</h4>
        <p><strong>Dr. Sarah Chen, AI</strong></p>
        <p>• Clinical analysis & emotional assessment<br>
        • Risk evaluation & pattern recognition<br>
        • Personalized situation understanding<br>
        • Evidence-based initial screening</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>🎯 Action Strategist</h4>
        <p><strong>Dr. Marcus Rodriguez, AI</strong></p>
        <p>• Immediate intervention planning<br>
        • Resource connection & referrals<br>
        • Crisis response coordination<br>
        • Actionable coping strategies</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>📈 Recovery Planner</h4>
        <p><strong>Dr. Emily Watson, AI</strong></p>
        <p>• Long-term support strategy<br>
        • Progress monitoring systems<br>
        • Relapse prevention planning<br>
        • Sustainable wellness routines</p>
    </div>
    """, unsafe_allow_html=True)

# Input form
st.markdown("### 📝 Personal Wellbeing Assessment")

with st.form("wellbeing_assessment"):
    col1, col2 = st.columns(2)
    
    with col1:
        mental_state = st.text_area(
            "Current Emotional State",
            placeholder="Describe how you've been feeling recently, any concerns, or thoughts you'd like to share...",
            height=120
        )
        
        sleep_hours = st.select_slider(
            "Average Sleep (hours per night)",
            options=list(range(0, 13)),
            value=7,
            format_func=lambda x: f"{x} hours"
        )
        
        stress_level = st.slider(
            "Current Stress Level",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very Low Stress, 10 = Extremely High Stress"
        )
    
    with col2:
        support_system = st.multiselect(
            "Current Support Network",
            ["Family Members", "Close Friends", "Professional Therapist", 
             "Support Groups", "Religious Community", "Workplace Support", "None Available"],
            help="Select all that apply to your current situation"
        )
        
        recent_changes = st.text_area(
            "Recent Life Changes",
            placeholder="Any significant events, transitions, or changes in the last 3-6 months...",
            height=80
        )
        
        symptoms = st.multiselect(
            "Current Symptoms or Concerns",
            ["Persistent Anxiety", "Depressed Mood", "Sleep Difficulties", 
             "Chronic Fatigue", "Loss of Interest", "Concentration Problems",
             "Appetite Changes", "Social Withdrawal", "Mood Swings", 
             "Physical Discomfort", "Panic Attacks", "Intrusive Thoughts"]
        )
    
    # Advanced options in expander
    with st.expander("📊 Additional Assessment Details"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            anxiety_level = st.slider("Anxiety Level (1-10)", 1, 10, 3)
            depression_level = st.slider("Depression Level (1-10)", 1, 10, 3)
            energy_level = st.slider("Energy Level (1-10)", 1, 10, 5)
        
        with col_b:
            social_connection = st.slider("Social Connection (1-10)", 1, 10, 5)
            work_satisfaction = st.slider("Work/Life Satisfaction (1-10)", 1, 10, 5)
            overall_wellbeing = st.slider("Overall Wellbeing (1-10)", 1, 10, 5)
    
    submit_button = st.form_submit_button(
        "🚀 Activate AI Mental Wellbeing Crew",
        use_container_width=True
    )

# Process the assessment
if submit_button:
    if not OPENAI_API_KEY:
        st.error("🔑 Please provide your OpenAI API key to activate the AI crew.")
    elif not mental_state.strip():
        st.error("📝 Please describe your current emotional state to get personalized support.")
    else:
        # Initialize OpenAI
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        
        # Create comprehensive user profile
        user_profile = f"""
        PERSONAL WELLBEING ASSESSMENT:
        
        Emotional State: {mental_state}
        Sleep Pattern: {sleep_hours} hours per night
        Stress Level: {stress_level}/10
        Support System: {', '.join(support_system) if support_system else 'Limited support network'}
        Recent Life Changes: {recent_changes if recent_changes else 'No significant changes reported'}
        Current Symptoms: {', '.join(symptoms) if symptoms else 'No specific symptoms reported'}
        
        DETAILED METRICS:
        - Anxiety Level: {anxiety_level}/10
        - Depression Indicators: {depression_level}/10
        - Energy Level: {energy_level}/10
        - Social Connection: {social_connection}/10
        - Work/Life Satisfaction: {work_satisfaction}/10
        - Overall Wellbeing: {overall_wellbeing}/10
        
        Assessment Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """
        
        # Create progress tracking
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        with st.spinner("🤖 Initializing AI Mental Wellbeing Crew..."):
            
            # Define the CrewAI agents
            assessment_agent = Agent(
                role="Mental Health Assessment Specialist",
                goal="Conduct comprehensive psychological assessment and emotional state analysis",
                backstory="""You are Dr. Sarah Chen, a licensed clinical psychologist with 15 years of experience 
                in mental health assessment. You specialize in evidence-based psychological evaluation, risk assessment, 
                and creating safe therapeutic spaces. Your approach combines clinical precision with genuine empathy, 
                helping individuals understand their mental health status with clarity and compassion.""",
                verbose=True,
                allow_delegation=False,
                llm=llm,
                max_iter=3
            )
            
            action_agent = Agent(
                role="Crisis Intervention and Action Planning Specialist",
                goal="Develop immediate, practical intervention strategies and connect individuals with appropriate resources",
                backstory="""You are Dr. Marcus Rodriguez, a crisis intervention specialist and clinical social worker 
                with expertise in emergency mental health response. You excel at creating actionable, personalized 
                intervention plans that respect individual capacity and circumstances. Your strength lies in translating 
                clinical recommendations into practical, achievable daily actions while ensuring appropriate resource connections.""",
                verbose=True,
                allow_delegation=False,
                llm=llm,
                max_iter=3
            )
            
            recovery_agent = Agent(
                role="Long-term Recovery and Wellness Planning Specialist",
                goal="Design sustainable, personalized long-term mental health recovery and maintenance strategies",
                backstory="""You are Dr. Emily Watson, a recovery-focused psychologist specializing in long-term 
                mental health planning and resilience building. With expertise in positive psychology and behavioral 
                change, you create comprehensive recovery roadmaps that evolve with individuals' growth. Your approach 
                emphasizes sustainable habits, progress tracking, and building internal resources for lasting wellness.""",
                verbose=True,
                allow_delegation=False,
                llm=llm,
                max_iter=3
            )
            
            # Define tasks for each agent
            assessment_task = Task(
                description=f"""
                Conduct a comprehensive mental health assessment based on the following user profile:
                
                {user_profile}
                
                Your assessment should include:
                1. Clinical evaluation of emotional state and psychological symptoms
                2. Risk assessment using evidence-based screening approaches
                3. Identification of strengths, protective factors, and areas of concern
                4. Analysis of current coping mechanisms and support systems
                5. Preliminary diagnostic considerations (if applicable)
                6. Clear, compassionate communication of findings to the user
                
                Format your response as a professional but accessible assessment report that validates 
                the user's experiences while providing clinical insights.
                """,
                agent=assessment_agent,
                expected_output="A comprehensive psychological assessment report (500-700 words) with clinical insights, risk evaluation, and supportive recommendations."
            )
            
            action_task = Task(
                description=f"""
                Based on the assessment findings, create an immediate action plan and resource connection strategy:
                
                User Profile: {user_profile}
                
                Your action plan should include:
                1. Immediate crisis response protocol (if needed)
                2. Evidence-based coping strategies tailored to specific symptoms
                3. Specific mental health resources with contact information
                4. Daily wellness action items with realistic time commitments
                5. Support network activation strategies
                6. Safety planning elements (if indicated)
                7. Professional referral recommendations with guidance on access
                
                Focus on practical, achievable actions that respect the user's current energy and capacity levels.
                """,
                agent=action_agent,
                expected_output="A detailed action plan (500-700 words) with immediate interventions, resources, and practical daily strategies.",
                context=[assessment_task]
            )
            
            recovery_task = Task(
                description=f"""
                Develop a comprehensive long-term recovery and wellness maintenance strategy:
                
                User Profile: {user_profile}
                
                Your recovery plan should include:
                1. Personalized long-term wellness goals with milestone markers
                2. Progressive skill-building curriculum for emotional regulation
                3. Relapse prevention strategy with trigger identification
                4. Support network expansion and maintenance protocols
                5. Self-monitoring systems and progress tracking methods
                6. Graduated self-care routine that evolves over time
                7. Professional care coordination and therapy recommendations
                8. Crisis prevention and early intervention strategies
                
                Create a sustainable roadmap that builds resilience and promotes lasting mental wellness.
                """,
                agent=recovery_agent,
                expected_output="A comprehensive long-term recovery plan (600-800 words) with sustainable strategies, progress milestones, and wellness maintenance protocols.",
                context=[assessment_task, action_task]
            )
            
            # Create and execute the crew
            mental_health_crew = Crew(
                agents=[assessment_agent, action_agent, recovery_agent],
                tasks=[assessment_task, action_task, recovery_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute with progress updates
            progress_bar.progress(25)
            status_placeholder.markdown("🔍 **Assessment Agent** analyzing your situation...")
            st.session_state.agent_status['assessment'] = 'working'
            
            time.sleep(1)  # Brief pause for demo effect
            
            progress_bar.progress(50)
            status_placeholder.markdown("🎯 **Action Agent** creating your intervention plan...")
            st.session_state.agent_status['assessment'] = 'complete'
            st.session_state.agent_status['action'] = 'working'
            
            time.sleep(1)
            
            progress_bar.progress(75)
            status_placeholder.markdown("📈 **Recovery Agent** designing your long-term strategy...")
            st.session_state.agent_status['action'] = 'complete'
            st.session_state.agent_status['followup'] = 'working'
            
            # Execute the crew
            try:
                result = mental_health_crew.kickoff()
                
                progress_bar.progress(100)
                status_placeholder.markdown("✅ **All Agents Complete** - Your personalized mental health plan is ready!")
                st.session_state.agent_status['followup'] = 'complete'
                
                # Store results
                st.session_state.crew_results = result
                
                time.sleep(1)
                status_placeholder.empty()
                progress_bar.empty()
                
            except Exception as e:
                st.error(f"❌ An error occurred during crew execution: {str(e)}")
                st.info("💡 This often happens with API rate limits. Please try again in a moment.")

# Display results if available
if st.session_state.crew_results:
    st.markdown("---")
    st.markdown("## 📋 Your Personalized Mental Wellbeing Plan")
    
    # Parse the crew results
    try:
        tasks_output = st.session_state.crew_results.tasks_output
        
        # Display each agent's output
        with st.expander("🔍 **Psychological Assessment Report**", expanded=True):
            st.markdown(tasks_output[0].raw)
        
        with st.expander("🎯 **Immediate Action Plan & Resources**", expanded=True):
            st.markdown(tasks_output[1].raw)
        
        with st.expander("📈 **Long-term Recovery Strategy**", expanded=True):
            st.markdown(tasks_output[2].raw)
        
        # Success message with metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>Assessment</h4>
                <p>✅ Complete</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>Action Plan</h4>
                <p>✅ Ready</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>Recovery Plan</h4>
                <p>✅ Activated</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.success("🌟 **Your AI Mental Wellbeing Crew has successfully created your personalized support plan!**")
        
        # Add download option
        st.markdown("### 💾 Save Your Plan")
        plan_text = f"""
        PERSONAL MENTAL WELLBEING PLAN
        Generated by AI Mental Wellbeing Crew
        Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        
        ASSESSMENT REPORT:
        {tasks_output[0].raw}
        
        ACTION PLAN:
        {tasks_output[1].raw}
        
        RECOVERY STRATEGY:
        {tasks_output[2].raw}
        
        ---
        This plan was generated by AI and should complement, not replace, professional mental health care.
        """
        
        st.download_button(
            label="📥 Download Complete Plan (PDF-ready text)",
            data=plan_text,
            file_name=f"mental_wellbeing_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")
        st.write("Raw results:", st.session_state.crew_results)

# Footer for auditorium demo
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;">
    <h3>🎭 Live Demo Complete</h3>
    <p><strong>AI Mental Wellbeing Crew - Powered by CrewAI</strong></p>
    <p>Multi-Agent AI System • Scalable Mental Health Support • Built for Impact</p>
    <p><em>Demonstrating the future of AI-assisted mental healthcare</em></p>
</div>
""", unsafe_allow_html=True)
