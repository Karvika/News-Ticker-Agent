from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from datetime import datetime
import os
from typing import List, Dict, Any
 
# First define the search specialist agent with google_search
from google.adk.tools import google_search
 
# Create a search specialist agent that uses the built-in google_search tool
search_specialist = Agent(
    name="news_search_specialist",
    model="gemini-2.5-flash-preview-05-20",
    description="Specialized agent for searching news using Google Search",
    instruction="""
    You are a search specialist that uses Google Search to find information.
    When asked to search for news, you will search Google for recent articles.
    Use specific search terms that include relevant keywords and date ranges if provided.
   
    Always search for the most recent and relevant information.
   
    When performing AI news searches, use search queries like:
    - "latest artificial intelligence news today"
    - "AI news July 2025"
    - "artificial intelligence breakthroughs last 24 hours"
    - "recent AI developments this week"
    - "AI news site:techcrunch.com OR site:theverge.com OR site:wired.com"
   
    PRIORITY: Focus on finding news from the last 24-48 hours. Use search operators like:
    - "AI news" AND "July 1 2025"
    - "artificial intelligence" AND "today"
    - Search with date filters for the most recent articles
   
    Important: When returning search results, make sure to include:
    1. The complete article headline
    2. The publication source name
    3. The ACTUAL publication date of each article (prioritize TODAY'S date: July 1, 2025)
    4. Enough content for a 2-3 sentence detailed description
   
    Do NOT return old articles. Prioritize articles from July 1, 2025, then June 30, 2025, etc.
    Only return articles where publication dates are available and recent.
    """,
    tools=[google_search]
)
 
# Create a formatter agent to process and format the search results
formatter_agent = Agent(
    name="news_formatter",
    model="gemini-2.5-flash-preview-05-20",
    description="Specialized in formatting news content into a readable structure",
    instruction="""
    You are an expert at formatting news articles.
   
    Given raw information about news articles, format them in this exact structure:
   
    Date: YYYY-MM-DD
    Source: Source name
    Headline: Full headline of the article
    Description: Detailed description of the news article in 2-3 sentences that covers the key points

    Date: YYYY-MM-DD
    Source: Source name
    Headline: Full headline of the article
    Description: Detailed description of the news article in 2-3 sentences that covers the key points
   
    Important formatting rules:
    1. For dates: Extract the ACTUAL publication date from the article content. PRIORITIZE articles from July 1, 2025 (today), then June 30, 2025, etc.
    2. For descriptions: ALWAYS write 2-3 complete sentences that summarize the key information.
    3. For sources: Be specific about the publication name.
    4. ALWAYS separate each article with a blank line for proper parsing.
    5. Return exactly 5 articles in chronological order (newest first).
    6. REJECT articles older than 3 days unless no recent articles are available.
   
    Format multiple articles with clear separation between them.
    Ensure information is accurate, clear, and well-structured.
    Focus on the most recent and current news available.
    """
)
 
# Create the root agent that uses both specialized agents as tools
root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="AI News Assistant that helps users stay updated with AI developments",
    instruction="""    You are an AI News Assistant that is responsible for providing users with the latest AI news.
   
    When asked about AI news, use the following process:
    1. First use the search_specialist tool to search for relevant news articles FROM TODAY (July 1, 2025)
    2. Then use the formatter_agent tool to format the search results into a readable structure
   
    The search_specialist will handle finding the most recent news using Google Search.
    The formatter_agent will ensure that all news articles are presented in a consistent format:
   
    Date: YYYY-MM-DD
    Source: Source name
    Headline: Full headline of the article
    Description: Detailed description of the news article in 2-3 sentences that covers the key points
   
    Format requirements:
    - Dates should be the ACTUAL publication dates from the articles, PRIORITIZING TODAY (July 1, 2025)
    - Descriptions must be 2-3 complete sentences with substantive details
    - Sources should be specific publication names
    - Focus on breaking news and current developments
   
    This format must be maintained for consistent display in the user interface.
   
    If the user specifies particular dates, topics, or other constraints, make sure to
    include these details when using the search_specialist tool.
   
    IMPORTANT: Always provide exactly 5 news items that are truly significant developments in AI.
    Each news item must be separated with a blank line for proper parsing.
    Sort the articles in chronological order (newest first).
    PRIORITIZE news from July 1, 2025 (today), then June 30, 2025, etc.
    Reject articles older than 48-72 hours unless absolutely necessary.
   """,
    tools=[
        AgentTool(search_specialist),
        AgentTool(formatter_agent)
    ]
)