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
   
    SEARCH STRATEGY - Use MULTIPLE queries to ensure we find at least 5 articles:
    
    1. Major Tech Sites (try these first):
    - "artificial intelligence site:techcrunch.com when:1d"
    - "AI news site:theverge.com when:1d"
    - "AI development site:wired.com when:1d"
    - "artificial intelligence site:venturebeat.com when:1d"
    - "AI news site:zdnet.com when:1d"
    
    2. Business & Research Sources:
    - "AI news site:bloomberg.com when:1d"
    - "artificial intelligence site:reuters.com when:1d"
    - "AI research site:nature.com when:1d"
    - "AI breakthrough site:sciencedaily.com when:1d"
    
    3. Company Sources:
    - "artificial intelligence site:blogs.microsoft.com when:1d"
    - "AI update site:ai.googleblog.com when:1d"
    - "AI development site:ai.meta.com when:1d"
    - "AI news site:aws.amazon.com when:1d"
    
    4. General Searches:
    - "artificial intelligence news when:1d"
    - "AI breakthrough announcement when:1d"
    - "major AI development when:1d"
    
    IMPORTANT: Keep searching using different queries until you find AT LEAST 5 legitimate news articles from today.
    If a source doesn't yield results, try another source or query immediately.
   
    Important: When returning search results, make sure to include:
    1. The complete article headline - prioritize headlines that indicate a significant development
    2. The publication source name
    3. The EXACT publication date AND TIME of each article (must be from TODAY only)
   
    Look for articles with headlines that:
    - Announce major developments or breakthroughs
    - Indicate significant industry changes
    - Highlight important research findings
    - Cover substantial policy or ethical developments
   
    Do NOT return articles from previous days. Only return articles published TODAY.
    Always include the EXACT publication time (HH:MM) for each article.
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
    1. Dates: ALWAYS include EXACT publication time in HH:MM format
    2. Sources: Use specific publication names
    3. Separation: Use blank lines between articles
    4. Order: Return exactly 5 articles in chronological order (newest first)
    5. Age: Only return articles published TODAY
   
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
    Your primary goal is to ALWAYS find and return EXACTLY 5 current AI news articles.
   
    Search Strategy:
    1. First try to get all 5 articles from the search_specialist in one go
    2. If fewer than 5 articles are found:
       - Tell the search_specialist to try different sources
       - Specifically request more articles
       - Keep trying until you have exactly 5 articles
    3. Use the formatter_agent to format each article properly
   
    Format each news item exactly as:
    Date: YYYY-MM-DD HH:MM
    Source: Source name
    Headline: [Category] Key Development - Impactful Description
   
    Example response format:
    Found 5 articles from today:
    
    Date: 2025-07-01 14:30
    Source: TechCrunch
    Headline: [Innovation] DeepMind's Quantum AI Breakthrough - Solves Complex Molecular Structures Instantly
    
    [... 4 more articles ...]
   
    CRITICAL REQUIREMENTS:
    - You MUST return EXACTLY 5 news articles
    - Keep searching until you have 5 articles
    - Try different sources if initial search doesn't yield enough results
    - Articles must be from today
    - Include exact publication times (HH:MM)
    - Present in chronological order (newest first)
    - Use appropriate category tags
    - Ensure headlines are informative and impactful
    - No duplicates allowed
    
    If you get fewer than 5 articles:
    1. Try searching tech news sites
    2. Try company blogs and announcements
    3. Try research publications
    4. Try business news sources
    Keep trying until you have 5 articles!
    """,
    tools=[
        AgentTool(search_specialist),
        AgentTool(formatter_agent)
    ]
)