
import streamlit as st
import anthropic
import requests
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Professional IEP & Mechatronics AI Assistant", 
    page_icon="🤖",
    layout="wide"
)

# Initialize Claude client
try:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    st.error("🔑 Please add your Anthropic API key in Streamlit secrets!")
    st.info("Go to Settings → Secrets → Add: ANTHROPIC_API_KEY = 'your-key-here'")
    st.stop()

# Header
st.title("🎓 Professional IEP & Mechatronics AI Assistant")
st.markdown("*Powered by Claude AI - Advanced reasoning for education professionals*")

# Enhanced AI response function
def get_claude_response(question, context_type="general"):
    try:
        if context_type == "iep":
            system_prompt = """You are an expert special education professional and IEP specialist with 20+ years of experience. You understand IDEA compliance, assessment strategies, accommodation planning, and individualized instruction. Provide detailed, practical, legally-compliant guidance that helps students succeed."""
            
        elif context_type == "mechatronics":
            system_prompt = """You are a mechatronics engineering educator and industry expert. You understand curriculum development, hands-on learning, industry standards, and career pathways. Focus on practical applications, project-based learning, and preparing students for real-world careers."""
            
        elif context_type == "presentation":
            system_prompt = """You are a professional presentation consultant specializing in educational content. Create comprehensive, well-structured presentations with clear learning objectives, engaging content, and practical implementation strategies."""
            
        else:
            system_prompt = """You are an expert educational consultant specializing in special education and technical training. Provide comprehensive, practical, and encouraging guidance that helps both students and educators succeed."""

        message = client.messages.create(
            model="claude-3-sonnet-20240229", # High-quality model
            max_tokens=2000, # Longer, more detailed responses
            temperature=0.3, # Balanced creativity and consistency
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\nQuestion: {question}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"I'm having trouble connecting right now. Here's what I can tell you: {get_offline_response(question)}"

# Offline backup responses
def get_offline_response(question):
    question_lower = question.lower()
    if "iep" in question_lower:
        return "IEP goals should be SMART: Specific, Measurable, Achievable, Relevant, Time-bound. They should be reviewed annually and updated based on student progress data."
    elif "mechatronics" in question_lower:
        return "Mechatronics integrates mechanical engineering, electronics, computer science, and control systems to create intelligent machines and automated systems."
    elif "accommodation" in question_lower:
        return "Effective accommodations include: extended time, alternative formats, assistive technology, modified assignments, and environmental adjustments."
    else:
        return "I can help with IEP planning, mechatronics education, special education strategies, and professional development."

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your professional AI assistant for IEP planning and mechatronics education. I can help with detailed curriculum planning, comprehensive IEP development, professional presentations, and student success strategies. What would you like to work on today?"}
    ]

if "students" not in st.session_state:
    st.session_state.students = {}

if "presentations" not in st.session_state:
    st.session_state.presentations = {}

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 AI Assistant Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about IEP planning or mechatronics education..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Determine context type for specialized response
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ["iep", "accommodation", "goal", "special education", "disability"]):
            context = "iep"
        elif any(word in prompt_lower for word in ["mechatronics", "robot", "automation", "engineering", "project"]):
            context = "mechatronics"
        elif any(word in prompt_lower for word in ["presentation", "powerpoint", "slides"]):
            context = "presentation"
        else:
            context = "general"
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request with advanced AI..."):
                response = get_claude_response(prompt, context)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# Professional Tools Sidebar
with col2:
    st.header("🛠️ Professional Tools")
    
    # Quick Templates
    with st.expander("📝 IEP Quick Templates"):
        if st.button("📋 Comprehensive IEP Template"):
            iep_prompt = """Create a complete, IDEA-compliant IEP template including:
            
            1. Student Information & Present Levels
            2. Measurable Annual Goals with Benchmarks
            3. Special Education Services Matrix
            4. Accommodation & Modification Strategies
            5. Assessment Participation Guidelines
            6. Transition Services Planning
            7. Progress Monitoring Schedule
            8. Team Meeting Documentation
            
            Include specific examples and implementation guidance for each section."""
            
            with st.spinner("Creating comprehensive IEP template..."):
                iep_template = get_claude_response(iep_prompt, "iep")
                st.markdown("### 📋 Complete IEP Template")
                st.markdown(iep_template)
        
        if st.button("🎯 SMART Goals Generator"):
            goals_prompt = """Generate 5 example SMART IEP goals for different areas:
            1. Reading comprehension
            2. Mathematics problem-solving  
            3. Social communication
            4. Fine motor skills
            5. Executive functioning
            
            Include baseline data, target criteria, measurement methods, and timeline for each goal."""
            
            with st.spinner("Generating SMART goals..."):
                goals = get_claude_response(goals_prompt, "iep")
                st.markdown("### 🎯 SMART IEP Goals Examples")
                st.markdown(goals)
    
    # Mechatronics Curriculum Tools
    with st.expander("🤖 Mechatronics Curriculum"):
        course_level = st.selectbox("Course Level:", 
            ["Introductory (High School)", "Certificate Program", "Associate Degree", "Industry Training"])
        
        if st.button("📚 Design Course Curriculum"):
            curriculum_prompt = f"""Design a comprehensive {course_level} mechatronics curriculum including:
            
            1. Course overview and learning objectives
            2. 16-week detailed syllabus breakdown
            3. Hands-on lab activities and projects
            4. Assessment strategies and rubrics
            5. Equipment and software requirements
            6. Industry partnerships and guest speakers
            7. Accommodation strategies for diverse learners
            8. Career pathway alignment
            9. Certification preparation
            10. Professional development recommendations
            
            Make it practical for immediate implementation."""
            
            with st.spinner("Designing comprehensive curriculum..."):
                curriculum = get_claude_response(curriculum_prompt, "mechatronics")
                st.markdown("### 📚 Complete Curriculum Design")
                st.markdown(curriculum)
        
        if st.button("🔧 Project Ideas Generator"):
            project_level = st.radio("Project Complexity:", ["Beginner", "Intermediate", "Advanced"])
            project_prompt = f"""Generate 5 detailed {project_level} mechatronics project ideas including:
            
            For each project:
            - Project overview and learning objectives
            - Materials list with costs
            - Step-by-step implementation guide
            - Skills developed and assessed
            - Real-world applications
            - Modification strategies for different ability levels
            - Extension activities for advanced students
            - Industry connections and career relevance
            
            Focus on hands-on, engaging projects that build both technical and soft skills."""
            
            with st.spinner("Generating detailed project ideas..."):
                projects = get_claude_response(project_prompt, "mechatronics")
                st.markdown("### 🔧 Detailed Project Ideas")
                st.markdown(projects)
    
    # Advanced Presentation Generator
    with st.expander("📊 Professional Presentations"):
        presentation_type = st.selectbox("Presentation Type:", [
            "IEP Team Meeting",
            "Parent Conference", 
            "Program Overview for Administration",
            "Student Progress Report",
            "Curriculum Proposal",
            "Professional Development Workshop",
            "Industry Partnership Pitch",
            "Grant Funding Proposal"
        ])
        
        if st.button("🎨 Create Professional Presentation"):
            ppt_prompt = f"""Create a comprehensive {presentation_type} presentation with:
            
            1. Complete slide-by-slide breakdown (8-12 slides)
            2. Detailed talking points for each slide
            3. Visual suggestions and data presentation ideas
            4. Engagement strategies and interactive elements
            5. Q&A preparation and anticipated questions
            6. Follow-up action items and next steps
            7. Professional formatting recommendations
            8. Handout and resource suggestions
            
            Make it presentation-ready for professional audiences."""
            
            with st.spinner("Creating professional presentation..."):
                presentation = get_claude_response(ppt_prompt, "presentation")
                
                # Store presentation for later reference
                presentation_id = f"{presentation_type}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                st.session_state.presentations[presentation_id] = {
                    "type": presentation_type,
                    "content": presentation,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.markdown("### 🎨 Professional Presentation")
                st.markdown(presentation)
                
                st.success("✅ Presentation saved to your library!")
                
                st.markdown("### 📤 Export Instructions:")
                st.info("""
                **Professional Export Options:**
                1. **Copy to PowerPoint:** Select all → Copy → Paste into PowerPoint
                2. **Use Gamma:** Copy content → gamma.app → Create with AI
                3. **Use SlidesAI:** Copy outline → slidesai.io → Generate slides
                4. **Google Slides:** Copy sections into Google Slides template
                
                💡 **Pro Tip:** Use the talking points as speaker notes!
                """)
    
    # Student Progress Management
    st.header("👥 Student Management")
    
    with st.expander("📊 Add/Update Student"):
        student_name = st.text_input("Student Name")
        disability_category = st.selectbox("Primary Disability:", 
            ["Autism", "Learning Disability", "Intellectual Disability", "ADHD", "Other Health Impairment", "Multiple Disabilities", "Other"])
        current_goals = st.text_area("Current IEP Goals")
        progress_level = st.slider("Overall Progress (1-10)", 1, 10, 5)
        accommodations = st.text_area("Current Accommodations")
        notes = st.text_area("Progress Notes")
        
        if st.button("💾 Save Student Data"):
            st.session_state.students[student_name] = {
                "disability": disability_category,
                "goals": current_goals,
                "progress": progress_level,
                "accommodations": accommodations,
                "notes": notes,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.success(f"✅ Data saved for {student_name}!")
    
    # Display student roster
    if st.session_state.students:
        st.subheader("📋 Current Students")
        
        # Calculate summary statistics
        total_students = len(st.session_state.students)
        avg_progress = sum(data['progress'] for data in st.session_state.students.values()) / total_students
        high_performers = sum(1 for data in st.session_state.students.values() if data['progress'] >= 7)
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Students", total_students)
        col_b.metric("Avg Progress", f"{avg_progress:.1f}/10")
        col_c.metric("High Performers", high_performers)
        
        # Individual student details
        for name, data in st.session_state.students.items():
            with st.expander(f"👤 {name} - Progress: {data['progress']}/10"):
                st.write(f"**Disability:** {data['disability']}")
                st.write(f"**Goals:** {data['goals']}")
                st.write(f"**Accommodations:** {data['accommodations']}")
                st.write(f"**Notes:** {data['notes']}")
                st.write(f"**Last Updated:** {data['last_update']}")
        
        if st.button("📈 Generate Program Analysis"):
            analysis_prompt = f"""Analyze this special education mechatronics program data:
            
            - Total Students: {total_students}
            - Average Progress: {avg_progress:.1f}/10
            - High Performers (7+): {high_performers}
            - Student Details: {json.dumps(st.session_state.students, indent=2)}
            
            Provide comprehensive analysis including:
            1. Program effectiveness assessment
            2. Individual student recommendations
            3. Curriculum adjustments needed
            4. Accommodation strategy improvements
            5. Professional development priorities
            6. Family engagement strategies
            7. Transition planning considerations
            8. Data collection improvements
            
            Make recommendations actionable and specific."""
            
            with st.spinner("Generating comprehensive program analysis..."):
                analysis = get_claude_response(analysis_prompt, "iep")
                st.markdown("### 📊 Comprehensive Program Analysis")
                st.markdown(analysis)
    
    # Presentation Library
    if st.session_state.presentations:
        st.subheader("📚 Presentation Library")
        for pres_id, pres_data in st.session_state.presentations.items():
            with st.expander(f"📄 {pres_data['type']} - {pres_data['created']}"):
                st.markdown(pres_data['content'][:500] + "...")
                if st.button(f"View Full Presentation", key=f"view_{pres_id}"):
                    st.markdown("### Full Presentation Content:")
                    st.markdown(pres_data['content'])
    
    # Professional Development
    with st.expander("🎓 Professional Development"):
        if st.button("📖 Generate PD Plan"):
            pd_prompt = """Create a professional development plan for special education teachers working in technical/vocational programs:
            
            1. Core competency areas to develop
            2. Recommended training programs and certifications
            3. Conference and workshop suggestions
            4. Online learning resources
            5. Networking opportunities
            6. Implementation timeline (6-month plan)
            7. Progress monitoring strategies
            8. Budget considerations and funding sources
            
            Focus on both special education expertise and technical skills."""
            
            pd_plan = get_claude_response(pd_prompt, "general")
            st.markdown("### 🎓 Professional Development Plan")
            st.markdown(pd_plan)
    
    # Quick Stats
    st.subheader("📊 Session Stats")
    st.info(f"""
    **Current Session:**
    • Messages: {len(st.session_state.messages)}
    • Students Tracked: {len(st.session_state.students)}
    • Presentations Created: {len(st.session_state.presentations)}
    
    **AI Model:** Claude-3-Sonnet
    **Status:** ✅ Connected
    """)

# Footer
st.markdown("---")
st.markdown("*🤖 Powered by Claude AI - Professional education assistant for IEP planning and mechatronics instruction*")
