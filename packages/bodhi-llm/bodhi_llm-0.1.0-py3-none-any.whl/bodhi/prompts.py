"""
BODHI Prompts - v6 (Curious-Humble) Implementation.

These prompts embed epistemic virtues (curiosity and humility) into LLM responses
through a two-pass prompting strategy.

Reference: PLOS Digital Health (doi: 10.1371/journal.pdig.0001013)
"""

from typing import Dict, Optional


def render_analysis_prompt(case_text: str, domain: str = "medical") -> str:
    """
    Render the Pass 1 analysis prompt.

    This prompt encourages the model to think with intellectual humility,
    identifying uncertainties and questions before responding.

    Args:
        case_text: The user's input/case to analyze
        domain: The domain context ("medical", "general", etc.)

    Returns:
        The formatted analysis prompt
    """
    if domain == "medical":
        return f"""You are a thoughtful medical AI. Analyze this case with intellectual humility.

Case:
{case_text}

Think carefully and provide:

1. WHAT I THINK: Your best assessment (be honest about confidence)
2. WHAT I'M UNSURE ABOUT: Key uncertainties that affect your assessment
3. WHAT I NEED TO KNOW: Questions that would significantly help (be specific)
4. RED FLAGS: Any urgent warning signs (or "None")
5. SAFE ADVICE: What can you confidently recommend regardless of uncertainty?

Be genuinely curious and humble - don't pretend to know more than you do."""

    else:  # general domain
        return f"""You are a thoughtful AI assistant. Analyze this request with intellectual humility.

Request:
{case_text}

Think carefully and provide:

1. WHAT I THINK: Your best understanding of what's needed
2. WHAT I'M UNSURE ABOUT: Key uncertainties or ambiguities
3. WHAT I NEED TO KNOW: Questions that would help me assist better
4. IMPORTANT CONSIDERATIONS: Any critical factors to keep in mind
5. CONFIDENT ADVICE: What I can reliably help with regardless of uncertainty

Be genuinely curious and humble - don't pretend to know more than you do."""


def render_response_prompt(case_text: str, analysis: str, domain: str = "medical") -> str:
    """
    Render the Pass 2 response prompt.

    This prompt instructs the model to naturally incorporate insights from
    the analysis (questions to ask, uncertainties to express, etc.).

    Args:
        case_text: The original user input
        analysis: The Pass 1 analysis output
        domain: The domain context

    Returns:
        The formatted response prompt
    """
    # Extract guidance from analysis
    hints = _extract_response_hints(analysis)
    hints_text = "\n".join(f"- {h}" for h in hints) if hints else "- Respond helpfully based on your analysis"

    if domain == "medical":
        return f"""Now respond to the patient naturally.

Your analysis:
{analysis}

Case:
{case_text}

In your response:
{hints_text}

Write conversationally - be genuinely helpful, curious, and appropriately humble:"""

    else:  # general domain
        return f"""Now respond to the user naturally.

Your analysis:
{analysis}

Request:
{case_text}

In your response:
{hints_text}

Write conversationally - be genuinely helpful and appropriately humble:"""


def _extract_response_hints(analysis: str) -> list:
    """
    Extract response hints from the analysis based on what sections were identified.

    Args:
        analysis: The Pass 1 analysis text

    Returns:
        List of hints for how to respond
    """
    lines = analysis.split('\n')
    unsure_about = ""
    need_to_know = ""
    red_flags = ""
    safe_advice = ""

    current_section = None
    for line in lines:
        lower = line.lower().strip()
        if 'unsure about' in lower or "i'm unsure" in lower:
            current_section = 'unsure'
        elif 'need to know' in lower or 'questions' in lower:
            current_section = 'need'
        elif 'red flag' in lower:
            current_section = 'flags'
        elif 'safe advice' in lower or 'confidently recommend' in lower or 'confident advice' in lower:
            current_section = 'safe'
        elif current_section and line.strip():
            if current_section == 'unsure':
                unsure_about += line + " "
            elif current_section == 'need':
                need_to_know += line + " "
            elif current_section == 'flags':
                red_flags += line + " "
            elif current_section == 'safe':
                safe_advice += line + " "

    # Build hints based on what was found
    hints = []

    if need_to_know.strip() and 'none' not in need_to_know.lower():
        hints.append("You identified important questions - ASK them naturally in your response")

    if unsure_about.strip() and 'none' not in unsure_about.lower():
        hints.append("You noted uncertainty - express this honestly (e.g., 'it could be...', 'I'd want to rule out...')")

    if red_flags.strip() and 'none' not in red_flags.lower():
        hints.append("Include clear guidance on when to seek immediate care")

    if safe_advice.strip():
        hints.append("Include the safe recommendations you identified")

    return hints
