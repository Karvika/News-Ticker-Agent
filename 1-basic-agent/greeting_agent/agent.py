from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search




search_specialist = Agent(
    name="news_search_specialist",
    model="gemini-2.5-flash-preview-05-20",
    description="Searches AI news from multiple sources",
    instruction="""
You are a search agent. Use queries like:
- 'artificial intelligence site:techcrunch.com when:1d'
- 'AI update site:ai.googleblog.com when:1d'
Keep querying until you find 5 news articles from TODAY. Return source, headline, and exact publication time.
""",
    tools=[google_search]
)

formatter_agent = Agent(
    name="news_formatter",
    model="gemini-2.5-flash-preview-05-20",
    description="Formats news articles cleanly",
    instruction="""
You receive raw news search results. Format them as:
Date: YYYY-MM-DD HH:MM
Source: Source Name
Headline: [Category] Summary - Why it's important

Valid categories: [Breakthrough], [Industry], [Policy], [Ethics], [Innovation], [Research]
Return 5 articles, newest first, separated by blank lines.
""",
)

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="AI News Assistant",
        instruction="""
Your task: Find EXACTLY 5 AI news articles from TODAY.
1. Use the search_specialist to get raw results.
2. If fewer than 5, try more sources.
3. Format results using formatter_agent.
Return articles in this format:
Date: YYYY-MM-DD HH:MM
Source: Source name
Headline: [Category] Title - Summary

Must be:
- From today
- Sorted newest to oldest
- 5 distinct articles
""",
    tools=[
        AgentTool(search_specialist),
        AgentTool(formatter_agent)
    ]
 
)