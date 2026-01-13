"""Content-related prompts for Threads."""


def reply_strategy(context: str) -> str:
    """Craft a thoughtful reply to a thread.

    Args:
        context: The original post or conversation context
    """
    return f"""Help me craft a thoughtful reply to this thread:

{context}

Guidelines:
- Be genuine and add value to the conversation
- Keep it concise but meaningful
- Match the tone of the original post
- Avoid generic responses like "Great post!"
- If disagreeing, be respectful and constructive
- Consider asking a follow-up question to continue the dialogue

Provide 2-3 reply options with different approaches."""


def content_ideas(niche: str, count: int = 5) -> str:
    """Generate content ideas for Threads.

    Args:
        niche: Your content niche or area of expertise
        count: Number of ideas to generate
    """
    return f"""Generate {count} engaging Threads post ideas for the following niche: {niche}

For each idea, provide:
1. A hook/opening line
2. The main content angle
3. A suggested call-to-action

Focus on:
- Topics that spark discussion
- Relatable experiences or observations
- Hot takes or unique perspectives
- Behind-the-scenes or personal insights
- Questions that encourage engagement

Mix different content types: opinions, tips, stories, questions."""


def analyze_engagement(metrics: str) -> str:
    """Analyze engagement metrics and suggest improvements.

    Args:
        metrics: Description of your current engagement metrics or recent post performance
    """
    return f"""Analyze these Threads engagement metrics and provide actionable insights:

{metrics}

Please provide:
1. Key observations about the performance
2. What's working well
3. Areas for improvement
4. Specific recommendations for:
   - Best posting times
   - Content types to focus on
   - Engagement tactics
   - Growth strategies

Base your analysis on Threads best practices and social media engagement principles."""
