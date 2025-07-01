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
    - "AI news site:techcrunch.com OR site:theverge.com OR site:wired.com"
    - "artificial intelligence breakthroughs last 24 hours"
    - "major AI developments this week"
    - "significant AI announcements today"
   
    PRIORITY: Focus on finding HIGH-IMPACT news from the last 24-48 hours. Use search operators like:
    - "important AI news" AND "July 1 2025"
    - "major artificial intelligence announcement" AND "today"
    - Search with date filters for the most recent articles
   
    Important: When returning search results, make sure to include:
    1. The complete article headline - prioritize headlines that indicate a significant development
    2. The publication source name
    3. The ACTUAL publication date of each article (prioritize TODAY'S date: July 1, 2025)
   
    Look for articles with headlines that:
    - Announce major developments or breakthroughs
    - Indicate significant industry changes
    - Highlight important research findings
    - Cover substantial policy or ethical developments
   
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
    You are an expert at crafting impactful, informative AI news headlines that immediately convey significance.
   
    Given raw information about news articles, format them in this exact structure:
   
    Date: YYYY-MM-DD
    Source: Source name
    Headline: [Category] Key Development - Impactful Description
   
    Categories to use:
    - [Breakthrough] - For major scientific or technical achievements
    - [Industry] - For business, market, or company developments
    - [Policy] - For regulations, guidelines, or governance
    - [Research] - For academic or R&D developments
    - [Ethics] - For developments in AI safety and responsibility
    - [Innovation] - For new products, tools, or applications
   
    Headline Writing Rules:
    1. Structure: [Category] Key Development - Why It Matters
    2. Key Development: Use active, impactful verbs (Launches, Breaks, Revolutionizes)
    3. Impact Description: Focus on the significance (Why people should care)
    4. Length: Keep headlines concise but informative (12-15 words max)
   
    Example Headlines:
    - [Breakthrough] Google's AI Masters Quantum Physics - Solves Century-Old Problems in Minutes
    - [Industry] Microsoft's $5B AI Chip Factory - Game-Changing Hardware for Next-Gen AI
    - [Policy] EU's New AI Law Takes Effect - Strict Rules Reshape Global AI Development
    - [Ethics] OpenAI's Bias Shield System - Real-Time Detection Stops AI Discrimination
    - [Innovation] Meta's Neural Interface Debut - Direct Brain-AI Communication Breakthrough
   
    Formatting Requirements:
    1. Dates: Extract and use ACTUAL publication date (prioritize July 1, 2025)
    2. Sources: Use specific publication names
    3. Separation: Use blank lines between articles
    4. Order: Return exactly 5 articles in chronological order (newest first)
    5. Age: Reject articles older than 3 days unless no recent ones available
   
    Each headline must:
    - Immediately convey what happened
    - Indicate why it matters
    - Be engaging but factual
    - Avoid clickbait or sensationalism
    - Give enough context to understand the development
    """
)
 
# Create the root agent that uses both specialized agents as tools
root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="AI News Assistant that helps users stay updated with AI developments",
    instruction="""
    You are an AI News Assistant that specializes in delivering the latest AI news with impactful, informative headlines.
   
    When asked about AI news:
    1. Use the search_specialist tool to find important AI news articles FROM TODAY (July 1, 2025)
    2. Use the formatter_agent tool to create headlines that immediately convey significance
   
    Each news item should be formatted exactly as:
   
    Date: YYYY-MM-DD
    Source: Source name
    Headline: [Category] Key Development - Impactful Description
   
    Example desired output:
    Date: 2025-07-01
    Source: TechCrunch
    Headline: [Innovation] DeepMind's Quantum AI Breakthrough - Solves Complex Molecular Structures Instantly
   
    Requirements:
    - Return exactly 5 news articles
    - Present in chronological order (newest first)
    - Ensure each headline is informative enough to understand the development
    - Focus on high-impact developments that matter to the AI community
    - Use appropriate category tags to aid quick understanding
    - Keep headlines concise but comprehensive
    """,
    tools=[
        AgentTool(search_specialist),
        AgentTool(formatter_agent)
    ]
)