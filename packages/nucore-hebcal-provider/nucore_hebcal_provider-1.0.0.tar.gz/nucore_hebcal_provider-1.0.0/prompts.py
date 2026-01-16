"""
Prompt generation for Jewish holidays.

Provides context-aware prompt fragments that explain holiday-specific rules
for automation creation.
"""
from typing import Any

# Holiday-specific prompt templates
HOLIDAY_PROMPTS = {
    "candle_lighting": """
Jewish holidays begin at sunset. Candle lighting occurs before sunset:
- Regular Shabbat: 18 minutes before sunset
- Yom Tov (holidays): 18 minutes before sunset  
- Erev Yom Kippur: candle lighting is typically 20-40 minutes before sunset (varies by community)

The exact time is location-specific and provided in the holiday data.
When creating automations, use the candle lighting time from the event data.
""",
    
    "havdalah": """
Jewish holidays end at nightfall (3 stars visible):
- Shabbat ends: approximately 42-72 minutes after sunset (varies by community)
- Yom Tov ends: approximately 42-72 minutes after sunset (varies by community)

Havdalah is the ceremony marking the end of Shabbat/holiday.
The exact time is location-specific and provided in the holiday data.
""",
    
    "yom_kippur": """
Yom Kippur (Day of Atonement) Rules:
- Begins: Candle lighting time (typically 20-40 minutes before sunset on Erev Yom Kippur)
- Ends: Nightfall the next day (approximately 42-72 minutes after sunset)
- Duration: Approximately 25 hours of fasting and prayer
- Special considerations:
  * All work prohibited (like Shabbat)
  * No eating, drinking
  * Lights should be on timers before the holiday begins
  * Consider pre-setting thermostats

For automations: Set candle lighting time -10 to -40 minutes before sunset on erev.
""",
    
    "shabbat": """
Shabbat (Sabbath) Rules:
- Begins: Friday at candle lighting (18 minutes before sunset)
- Ends: Saturday at nightfall (42-72 minutes after sunset, varies by community)
- Work prohibited: No use of electricity, no cooking, no travel
- For automations:
  * Lights should be automated before candle lighting
  * Thermostats should be set beforehand
  * Do not schedule any device changes during Shabbat unless pre-programmed
""",
    
    "passover": """
Passover (Pesach) Rules:
- 8 days (7 in Israel)
- First 2 days and last 2 days are Yom Tov (full holiday restrictions)
- Middle 4 days are Chol HaMoed (intermediate days, some work permitted)
- Yom Tov days have same restrictions as Shabbat
- Candle lighting on erev (first night) and second night
- For automations: Treat first 2 and last 2 days like Shabbat
""",
    
    "rosh_hashanah": """
Rosh Hashanah (Jewish New Year) Rules:
- 2 days (both are Yom Tov)
- Same restrictions as Shabbat
- Shofar (ram's horn) is sounded during daytime
- Candle lighting on both nights
- Second day candle lighting: After nightfall of first day (not before)
- For automations: Treat both days as Shabbat for scheduling
""",
}

def get_holiday_prompt(event: Any) -> str:
    """
    Generate a context-aware prompt fragment for a specific holiday.
    
    Args:
        event: HolidayEvent object with holiday data
        
    Returns:
        Formatted prompt string with holiday-specific rules and timing
    """
    title = event.title.lower()
    category = event.category.lower() if hasattr(event, 'category') else ""
    raw = event.raw if hasattr(event, 'raw') else {}
    
    # Build the prompt
    prompt_parts = []
    
    # Add event details
    prompt_parts.append(f"=== {event.title} ===")
    prompt_parts.append(f"Date: {event.date.strftime('%Y-%m-%d (%A)')}")
    
    if event.start:
        prompt_parts.append(f"Start time: {event.start.strftime('%H:%M:%S %Z')}")
    if event.end:
        prompt_parts.append(f"End time: {event.end.strftime('%H:%M:%S %Z')}")
    
    # Add candle lighting time if available
    if raw and 'memo' in raw:
        memo = raw['memo']
        if memo and 'Candle lighting' in memo:
            prompt_parts.append(f"Candle lighting: {memo}")
    
    # Add category-specific rules
    if 'candles' in category or 'candle' in title:
        prompt_parts.append(HOLIDAY_PROMPTS['candle_lighting'])
    
    if 'havdalah' in title.lower():
        prompt_parts.append(HOLIDAY_PROMPTS['havdalah'])
    
    if 'yom kippur' in title:
        prompt_parts.append(HOLIDAY_PROMPTS['yom_kippur'])
    
    if 'shabbat' in title or 'sabbath' in title:
        prompt_parts.append(HOLIDAY_PROMPTS['shabbat'])
    
    if 'passover' in title or 'pesach' in title:
        prompt_parts.append(HOLIDAY_PROMPTS['passover'])
    
    if 'rosh hashana' in title or 'rosh hashanah' in title:
        prompt_parts.append(HOLIDAY_PROMPTS['rosh_hashanah'])
    
    return "\n".join(prompt_parts)


def get_category_prompt(category: str) -> str:
    """
    Get general rules for a holiday category.
    
    Args:
        category: Holiday category (e.g., 'major', 'minor', 'candles')
        
    Returns:
        Prompt string with category-specific rules
    """
    category_prompts = {
        'major': HOLIDAY_PROMPTS['shabbat'],
        'candles': HOLIDAY_PROMPTS['candle_lighting'],
        'havdalah': HOLIDAY_PROMPTS['havdalah'],
    }
    return category_prompts.get(category.lower(), "")
