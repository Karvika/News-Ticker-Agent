from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), 'greeting_agent', '.env')
load_dotenv(env_path)

app = Flask(__name__)
CORS(app)

try:
    from greeting_agent.agent import root_agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️ GOOGLE_API_KEY not found.")
        ADK_AVAILABLE = False
    else:
        # Create a simple session service
        session_service = InMemorySessionService()
        
        # Create runner with required session service
        runner = Runner(
            agent=root_agent,
            app_name="AI_News_Assistant",
            session_service=session_service  # Required argument
        )
        ADK_AVAILABLE = True

except ImportError as e:
    print(f"ADK imports failed: {e}")
    ADK_AVAILABLE = False
    root_agent = None
    runner = None

def decode_bytes(output):
    """Helper function to ensure serialization-safe output by decoding any bytes objects"""
    if isinstance(output, bytes):
        return output.decode('utf-8', errors='ignore')
    elif isinstance(output, dict):
        return {k: decode_bytes(v) for k, v in output.items()}
    elif isinstance(output, list):
        return [decode_bytes(i) for i in output]
    else:
        return output

async def run_agent_async(user_message):
    if not ADK_AVAILABLE:
        now = datetime.now()
        return "\n\n".join([
            f"Date: {now.strftime('%Y-%m-%d %H:%M')}\nSource: Mock Source {i+1}\nHeadline: [Test] Mock News {i+1}"
            for i in range(5)
        ])

    try:
        # Create content with the message and force refresh
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = types.Content(
            role="user", 
            parts=[types.Part(text=f"{user_message}\n[Refresh timestamp: {timestamp}]")]
        )
        
        # Initialize response
        final_response = []
        
        # Create a temporary session for this request
        session = session_service.create_session(
            app_name="AI_News_Assistant",
            user_id="news_user",
            state={}
        )
        
        # Run the agent with minimal context
        async for event in runner.run_async(
            user_id="news_user",
            session_id=session.id,
            new_message=content
        ):
            if hasattr(event, 'content') and event.content:
                for part in getattr(event.content, 'parts', []):
                    if hasattr(part, 'text'):
                        text = part.text
                        if isinstance(text, (str, bytes)):
                            final_response.append(decode_bytes(text))
        
        # Clean up the temporary session
        try:
            session_service.delete_session(
                app_name="AI_News_Assistant",
                user_id="news_user",
                session_id=session.id
            )
        except Exception as e:
            print(f"Session cleanup warning: {e}")
        
        # Join all response parts
        complete_response = ''.join(final_response)
        
        if not complete_response:
            raise Exception("No response received from agent")
            
        return complete_response
        
    except Exception as e:
        print(f"Error in run_agent_async: {str(e)}")
        raise

def run_agent_sync(user_message):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_agent_async(user_message))
        loop.close()
        return result
    except Exception as e:
        return f"Error: {e}"

def parse_news_data(news_text):
    news_items = []
    current_item = {}
    articles = [a.strip() for a in news_text.split("\n\n") if a.strip()]
    for article in articles:
        lines = [line.strip() for line in article.split("\n") if line.strip()]
        for line in lines:
            if line.startswith("Date:"):
                current_item["date"] = line.replace("Date:", "").strip()
            elif line.startswith("Source:"):
                current_item["source"] = line.replace("Source:", "").strip()
            elif line.startswith("Headline:"):
                current_item["headline"] = line.replace("Headline:", "").strip()
        if all(k in current_item for k in ["date", "source", "headline"]):
            news_items.append(current_item.copy())
            current_item = {}
    return news_items

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/news')
def get_news():
    try:
        print("Getting news request...")
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        user_prompt = (
            f"IMPORTANT: Find EXACTLY 5 AI news articles from today ({current_date}). "
            "Search multiple sources if needed: tech sites, company blogs, research sites, and business news. "
            f"Include exact publication times. Sort by newest first. Current time: {current_time}"
        )
        
        print("Using REAL data mode")
        
        # Run agent
        response = run_agent_sync(user_prompt)
        print("\n=== Raw Response ===")
        print(f"Type: {type(response)}")
        print("Content:", response)
        
        # Decode any bytes in the response
        safe_response = decode_bytes(response)
        print("\n=== Decoded Response ===")
        print(f"Type: {type(safe_response)}")
        print("Content:", safe_response)
        
        # Parse the response
        news_data = parse_news_data(safe_response)
        print("\n=== Parsed News Data ===")
        print(f"Type: {type(news_data)}")
        print("Content:", news_data)
        
        if not news_data:
            print("Warning: No news data parsed from response")
            print("Raw response:", safe_response)
            # If we got an error response, raise it
            if isinstance(safe_response, str) and safe_response.startswith("Error:"):
                raise Exception(safe_response)
            return jsonify([])
            
        return jsonify(news_data)
        
    except Exception as e:
        print(f"Error in get_news: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    # Simply get fresh news
    return get_news()

if __name__ == '__main__':
    print("✅ AI News Assistant is starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
