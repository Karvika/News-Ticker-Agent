from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from greeting_agent directory
env_path = os.path.join(os.path.dirname(__file__), 'greeting_agent', '.env')
load_dotenv(env_path)

app = Flask(__name__)
CORS(app)

# Simplified approach - try to import and handle gracefully
try:
    from greeting_agent.agent import root_agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    
    # Check if API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables")
        print("📝 Please create a .env file with your Google API key")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Google API key to GOOGLE_API_KEY")
        print("   3. Get your API key from: https://aistudio.google.com/app/apikey")
        ADK_AVAILABLE = False
    else:
        # Initialize session service and runner
        session_service = InMemorySessionService()
        runner = Runner(
            agent=root_agent,
            app_name="AI_News_Assistant",
            session_service=session_service,
        )
        
        # Global session management
        GLOBAL_SESSION_ID = None
        GLOBAL_USER_ID = "news_ticker_user"
        ADK_AVAILABLE = True
    
except ImportError as e:
    print(f"ADK imports failed: {e}")
    print("Running in mock mode - install dependencies first")
    ADK_AVAILABLE = False
    root_agent = None
    session_service = None
    runner = None

def get_or_create_session():
    """Get or create a global session for the news ticker"""
    if not ADK_AVAILABLE:
        return "mock_session"
        
    global GLOBAL_SESSION_ID
    
    if GLOBAL_SESSION_ID is None:
        # Create a new session
        session = session_service.create_session(
            app_name="AI_News_Assistant",
            user_id=GLOBAL_USER_ID,
            state={}
        )
        GLOBAL_SESSION_ID = session.id
        return session.id
    
    # Try to get existing session
    try:
        session_service.get_session(
            app_name="AI_News_Assistant", 
            user_id=GLOBAL_USER_ID, 
            session_id=GLOBAL_SESSION_ID
        )
        return GLOBAL_SESSION_ID
    except:
        # Session not found, create a new one
        session = session_service.create_session(
            app_name="AI_News_Assistant",
            user_id=GLOBAL_USER_ID,
            state={}
        )
        GLOBAL_SESSION_ID = session.id
        return session.id

async def run_agent_async(user_message):
    """Run the agent asynchronously"""
    if not ADK_AVAILABLE:
        return """Date: 2025-07-01
Source: TechCrunch
Headline: Major AI Breakthrough Announced by Leading Tech Company
Description: Researchers have announced a significant advancement in artificial intelligence technology that could revolutionize how we interact with digital systems. The new approach promises improved efficiency and better user experiences.

Date: 2025-07-01
Source: Wired
Headline: AI Safety Measures Implemented Across Major Platforms
Description: Technology companies are implementing new safety protocols for AI systems following recent regulatory guidelines. These measures aim to ensure responsible AI development and deployment across various industries.

Date: 2025-06-30
Source: The Verge
Headline: New AI Model Shows Promising Results in Healthcare Applications
Description: A recently developed AI model has demonstrated exceptional performance in medical diagnosis and treatment planning. Clinical trials show significant improvements in accuracy and efficiency compared to traditional methods.

Date: 2025-06-30
Source: MIT Technology Review
Headline: Quantum Computing Meets AI in Groundbreaking Research
Description: Scientists have successfully integrated quantum computing principles with artificial intelligence algorithms, potentially unlocking new capabilities in machine learning and data processing.

Date: 2025-06-29
Source: IEEE Spectrum
Headline: Open Source AI Framework Gains Industry Adoption
Description: A new open-source artificial intelligence framework is being adopted by major technology companies, promising to democratize AI development and foster innovation across the industry."""
    
    try:
        # Use global session management
        session_id = get_or_create_session()
            
        # Create content for the message
        content = types.Content(role="user", parts=[types.Part(text=user_message)])
        
        # Run the agent and collect response
        final_response = None
        async for event in runner.run_async(
            user_id=GLOBAL_USER_ID, 
            session_id=session_id, 
            new_message=content
        ):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text
                            break
                elif hasattr(event.content, 'text'):
                    final_response = event.content.text
        
        return final_response or "No response received from agent"
        
    except Exception as e:
        print(f"Error in run_agent_async: {str(e)}")  # Debug logging
        return f"Error: {str(e)}"

def run_agent_sync(user_message):
    """Run the agent in a synchronous context"""
    if not ADK_AVAILABLE:
        # Return mock data directly (not async)
        return """Date: 2025-07-01
Source: TechCrunch
Headline: Major AI Breakthrough Announced by Leading Tech Company
Description: Researchers have announced a significant advancement in artificial intelligence technology that could revolutionize how we interact with digital systems. The new approach promises improved efficiency and better user experiences.

Date: 2025-07-01
Source: Wired
Headline: AI Safety Measures Implemented Across Major Platforms
Description: Technology companies are implementing new safety protocols for AI systems following recent regulatory guidelines. These measures aim to ensure responsible AI development and deployment across various industries.

Date: 2025-06-30
Source: The Verge
Headline: New AI Model Shows Promising Results in Healthcare Applications
Description: A recently developed AI model has demonstrated exceptional performance in medical diagnosis and treatment planning. Clinical trials show significant improvements in accuracy and efficiency compared to traditional methods.

Date: 2025-06-30
Source: MIT Technology Review
Headline: Quantum Computing Meets AI in Groundbreaking Research
Description: Scientists have successfully integrated quantum computing principles with artificial intelligence algorithms, potentially unlocking new capabilities in machine learning and data processing.

Date: 2025-06-29
Source: IEEE Spectrum
Headline: Open Source AI Framework Gains Industry Adoption
Description: A new open-source artificial intelligence framework is being adopted by major technology companies, promising to democratize AI development and foster innovation across the industry."""
        
    try:
        print(f"Running agent with message: {user_message[:100]}...")  # Debug logging
        
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the agent
        response = loop.run_until_complete(run_agent_async(user_message))
        loop.close()
        
        print(f"Agent response: {response[:200]}...")  # Debug logging
        return response
    except Exception as e:
        print(f"Error in run_agent_sync: {str(e)}")  # Debug logging
        if 'loop' in locals():
            loop.close()
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """Get latest AI news"""
    try:
        print("Getting news request...")  # Debug logging
        
        # Get response from agent with a specific news request
        agent_response = run_agent_sync("Get me exactly 5 of the most recent AI news articles published TODAY (July 1, 2025) or within the last 24-48 hours. Include exact publication dates, sources, headlines, and detailed descriptions. Prioritize breaking news and current developments. Sort them by publication date with the newest first.")
        
        print(f"Agent response received: {len(agent_response)} characters")  # Debug logging
        
        return jsonify({
            'news': agent_response,
            'status': 'success',
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        print(f"Error in get_news: {str(e)}")  # Debug logging
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': str(datetime.now())
        }), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    """Manually refresh news"""
    return get_news()

if __name__ == '__main__':
    if ADK_AVAILABLE:
        print("✅ AI News Assistant starting with full ADK integration...")
        print("🤖 Your agent is ready to fetch real-time AI news!")
    else:
        print("⚠️  AI News Assistant starting in DEMO mode...")
        print("📦 Install missing dependencies:")
        print("   pip install deprecated")
        print("   pip install flask flask-cors")
        print("🎯 Demo mode will show sample news data")
    
    print("🌐 Visit http://localhost:5000 to access the news ticker")
    print("🔄 Auto-refresh every 5 minutes")
    app.run(debug=True, host='0.0.0.0', port=5000)
