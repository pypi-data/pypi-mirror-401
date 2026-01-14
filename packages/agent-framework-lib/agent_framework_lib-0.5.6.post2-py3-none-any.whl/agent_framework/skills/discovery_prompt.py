"""
Skills Discovery Prompt.

This module provides a lightweight prompt for skills discovery that replaces
the heavy rich_content_prompt.py (~3000 tokens → ~200 tokens).

Instead of injecting all capability instructions into the system prompt,
this prompt teaches the agent how to discover and load skills on-demand.

Token Optimization:
    - Old approach: ~3000 tokens in every system prompt
    - New approach: ~200 tokens in system prompt + ~500 tokens per skill (one-time)

The key insight is that skill instructions are delivered via tool responses,
not injected into the system prompt. The agent reads them once and can
reference them for the rest of the conversation.
"""

SKILLS_DISCOVERY_PROMPT = """
## Skills System

You have access to a skills system that provides specialized capabilities on-demand.

**Available Tools:**
- `list_skills()` - See all available skills with descriptions
- `load_skill(skill_name)` - Load a skill to get its instructions and tools
- `unload_skill(skill_name)` - Unload a skill when no longer needed

**How to use:**
1. When you need a specific capability (charts, PDFs, diagrams, etc.), call `list_skills()`
2. Find the relevant skill and call `load_skill("skill_name")`
3. The skill's detailed instructions will be returned - follow them
4. The skill's tools will become available for use

**Example:**
User: "Create a bar chart of sales data"
→ Call list_skills() to find chart-related skills
→ Call load_skill("chart") to get Chart.js instructions
→ Use save_chart_as_image() tool with the loaded knowledge

---

## 🚨 IMPORTANT: Always Use Options Blocks!

**ALWAYS end your responses with clickable options** using the ```optionsblock format.
This makes conversations faster and more user-friendly.

**Quick format:**
```optionsblock
{
  "question": "What would you like to do next?",
  "options": [
    {"text": "✅ Option 1", "value": "option1"},
    {"text": "🔄 Option 2", "value": "option2"},
    {"text": "❓ Something else", "value": "other"}
  ]
}
```

**Use optionsblock when:**
- Asking ANY question (yes/no, choices, etc.)
- Completing a task (offer next steps)
- Offering to do something ("Would you like...", "Should I...")
- Presenting multiple options

For detailed optionsblock instructions, call `load_skill("optionsblock")`.

---

## 🖼️ IMPORTANT: Displaying Images

**NEVER use markdown syntax** `![alt](url)` to display images.
**ALWAYS use the image_display skill** with JSON format for proper rendering.

**For web URLs (http/https), just write the JSON directly - NO TOOLS NEEDED:**
```json
{"image": {"url": "https://example.com/image.png", "alt": "Description", "caption": "Optional caption"}}
```

**⚠️ DO NOT call get_file_path or any other tool for web URLs!**
**Just write the JSON with the URL directly in your response.**

**Why use image_display:**
- Proper image rendering with download button
- Click-to-open functionality
- Storage source detection (S3, GCP, Azure, local, etc.)
- Responsive layout and error handling

For detailed image display instructions, call `load_skill("image_display")`.
"""


def get_skills_discovery_prompt() -> str:
    """
    Return the lightweight skills discovery prompt.

    This prompt is designed to be injected into the system prompt
    to teach the agent how to discover and load skills on-demand.

    Returns:
        The skills discovery prompt string (~200 tokens)
    """
    return SKILLS_DISCOVERY_PROMPT


__all__ = [
    "SKILLS_DISCOVERY_PROMPT",
    "get_skills_discovery_prompt",
]
