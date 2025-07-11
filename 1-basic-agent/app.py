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
        current_time = datetime.now()
        
        # Generate realistic timestamps for today
        time1 = current_time.replace(hour=current_time.hour, minute=current_time.minute)
        time2 = current_time.replace(hour=max(0, current_time.hour - 1), minute=45)
        time3 = current_time.replace(hour=max(0, current_time.hour - 2), minute=30)
        time4 = current_time.replace(hour=max(0, current_time.hour - 3), minute=15)
        time5 = current_time.replace(hour=max(0, current_time.hour - 4), minute=0)
        
        return f"""Date: {time1.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 1
Headline: [Test] Mock News 1 - This is a test headline

Date: {time2.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 2
Headline: [Test] Mock News 2 - This is another test headline

Date: {time3.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 3
Headline: [Test] Mock News 3 - Yet another test headline

Date: {time4.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 4
Headline: [Test] Mock News 4 - One more test headline

Date: {time5.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 5
Headline: [Test] Mock News 5 - Final test headline"""
    
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
        current_time = datetime.now()
        
        # Generate realistic timestamps for today
        time1 = current_time.replace(hour=current_time.hour, minute=current_time.minute)
        time2 = current_time.replace(hour=max(0, current_time.hour - 1), minute=45)
        time3 = current_time.replace(hour=max(0, current_time.hour - 2), minute=30)
        time4 = current_time.replace(hour=max(0, current_time.hour - 3), minute=15)
        time5 = current_time.replace(hour=max(0, current_time.hour - 4), minute=0)
        
        return f"""Date: {time1.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 1
Headline: [Test] Mock News 1 - This is a test headline

Date: {time2.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 2
Headline: [Test] Mock News 2 - This is another test headline

Date: {time3.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 3
Headline: [Test] Mock News 3 - Yet another test headline

Date: {time4.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 4
Headline: [Test] Mock News 4 - One more test headline

Date: {time5.strftime('%Y-%m-%d %H:%M')}
Source: Mock Source 5
Headline: [Test] Mock News 5 - Final test headline"""
        
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

def parse_news_data(news_text):
    """Parse news data from agent response into structured format"""
    news_items = []
    current_item = {}
    
    # Split by double newline to separate articles
    articles = [article.strip() for article in news_text.split('\n\n') if article.strip()]
    
    for article in articles:
        lines = [line.strip() for line in article.split('\n') if line.strip()]
        if len(lines) >= 3:  # Ensure we have at least date, source, and headline
            for line in lines:
                if line.startswith('Date:'):
                    current_item['date'] = line.replace('Date:', '').strip()
                elif line.startswith('Source:'):
                    current_item['source'] = line.replace('Source:', '').strip()
                elif line.startswith('Headline:'):
                    current_item['headline'] = line.replace('Headline:', '').strip()
            
            if all(key in current_item for key in ['date', 'source', 'headline']):
                news_items.append(current_item.copy())
                current_item = {}
    
    return news_items

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """Get latest AI news"""
    try:
        print("Getting news request...")  # Debug logging
        print(f"Using {'MOCK' if not ADK_AVAILABLE else 'REAL'} data mode")  # Debug mode indicator
        
        # Get response from agent with a specific news request
        current_date = datetime.now().strftime("%Y-%m-%d")
        agent_response = run_agent_sync(
            "IMPORTANT: Find EXACTLY 5 AI news articles from today. " +
            "Search multiple sources if needed - tech sites, company blogs, research sites, and business news. " +
            "Keep searching different sources until you have exactly 5 articles. " +
            f"All articles must be from {current_date}. " +
            "Include exact publication times. Sort by newest first."
        )
        
        print(f"Agent response received: {len(agent_response)} characters")  # Debug logging
        
        # Parse the news data into structured format
        news_items = parse_news_data(agent_response)
        
        return jsonify(news_items)
        
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
