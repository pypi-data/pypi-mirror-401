from __future__ import annotations

import aiohttp
from typing import List, Optional
from datetime import datetime
from nucore_holiday_provider import NuCoreHolidayProvider, HolidayEvent

from prompts import get_holiday_prompt


class HebcalProvider(NuCoreHolidayProvider):
    """Hebcal Jewish Holiday Provider for NuCore."""
    
    def __init__(self, tz_str: str, latitude: float, longitude: float):
        """Initialize Hebcal provider with location and timezone."""
        super().__init__(tz_str, latitude, longitude)
        self.base_url = "https://www.hebcal.com/hebcal"
    
    async def _get_prompt(self) -> str:
        """
        Descriptive information about this holiday provider.
        """
        return (
            "This provider supplies Jewish holidays and observances based on the Hebrew calendar and have specific observance rules. "
            "Shabbat along with most holidays begin at sunset (local time) and end at nightfall (local time) the next day. "
            "Major holidays (Yom Tov) include: Rosh Hashanah, Yom Kippur, Passover, Sukkot, Hanukkah, Purim, Shavuot, Tisha B'Av, and others. "
            )

    async def _format_holidays(self, holidays: List[HolidayEvent]) -> str:
        """
        Format a list of HolidayEvent objects into a readable string.
        
        :param holidays: List of HolidayEvent objects
        :return: Formatted string
        """
        if not holidays:
            return "No holidays found for the specified criteria."

        formatted_lines = []
        for holiday in holidays:
            line = f"{get_holiday_prompt(holiday)}"
            formatted_lines.append(line)
        
        formatted_lines.append("""
            General Jewish Holiday Timing:
            - Most Jewish holidays begin at sunset and end at nightfall the next day
            - Major holidays (Yom Tov) have the same restrictions as Shabbat
            - For automation purposes, schedule changes before the holiday begins
            """)
    
        return "\n".join(formatted_lines)
    
    async def _get_holidays( self, event: Optional[str], start_year: int, end_year: int, start_month: Optional[int], end_month: Optional[int]) -> List[HolidayEvent]:
        """
        Get holidays from Hebcal API with filters.
        
        :param event: Event name filter (substring match) - if None, no filter
        :param start_year: Starting year (inclusive)
        :param end_year: Ending year (inclusive)
        :param start_month: Starting month (1-12) - if None, no filter
        :param end_month: Ending month (1-12) - if None, no filter
        :return: List of HolidayEvent objects
        """
        all_holidays = []

        if end_year == None:
            end_year = start_year 
        # Fetch holidays for each year in range
        for year in range(start_year, end_year + 1):
            params = {
                "v": "1",
                "cfg": "json",
                "year": year,
                "maj": "on",  # Major holidays
                "min": "on",  # Minor holidays
                "mod": "on",  # Modern holidays
                "nx": "on",   # Rosh Chodesh
                "ss": "on",   # Special Shabbat
                "mf": "on",   # Minor fasts
                "c": "on",    # Candle lighting times
                "geo": "pos",
                "latitude": self.latitude,
                "longitude": self.longitude,
                "tzid": self.tz_str,
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            holidays = self._parse_hebcal_response(data)
                            all_holidays.extend(holidays)
            except Exception as e:
                # Log error but continue processing other years
                print(f"Error fetching Hebcal data for year {year}: {e}")
                continue
        
        # Apply filters
        filtered_holidays = self._apply_filters(
            all_holidays, event, start_month, end_month
        )
        
        return filtered_holidays
    
    def _parse_hebcal_response(self, data: dict) -> List[HolidayEvent]:
        """
        Parse Hebcal API response into HolidayEvent objects.
        
        :param data: JSON response from Hebcal API
        :return: List of HolidayEvent objects
        """
        holidays = []
        
        if "items" not in data:
            return holidays
        
        for item in data["items"]:
            try:
                # Parse the date
                date_str = item.get("date")
                if not date_str:
                    continue
                
                date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                
                # Create holiday event
                holiday = HolidayEvent(
                    date=date_obj.date(),
                    title=item.get("title", "Unknown"),
                    category=item.get("category", ""),
                    start=date_obj,
                    end=date_obj,
                    raw={
                        "hebrew": item.get("hebrew"),
                        "link": item.get("link"),
                        "memo": item.get("memo"),
                        "yomtov": item.get("yomtov"),
                        "subcat": item.get("subcat"),
                    }
                )
                
                holidays.append(holiday)
            except Exception as e:
                # Skip malformed entries
                print(f"Error parsing holiday item: {e}")
                continue
        
        return holidays
    
    def _apply_filters(
        self,
        holidays: List[HolidayEvent],
        event: Optional[str],
        start_month: Optional[int],
        end_month: Optional[int]
    ) -> List[HolidayEvent]:
        """
        Apply filters to holiday list.
        
        :param holidays: List of holidays to filter
        :param event: Event name filter (substring match)
        :param start_month: Starting month (1-12)
        :param end_month: Ending month (1-12)
        :return: Filtered list of holidays
        """
        filtered = holidays
        
        # Filter by event name
        if event:
            filtered = [
                h for h in filtered 
                if event.lower() in h.title.lower()
            ]
        
        # Filter by month range
        if start_month is not None and end_month is not None:
            filtered = [
                h for h in filtered
                if start_month <= h.date.month <= end_month
            ]
        elif start_month is not None:
            filtered = [
                h for h in filtered
                if h.date.month >= start_month
            ]
        elif end_month is not None:
            filtered = [
                h for h in filtered
                if h.date.month <= end_month
            ]
        
        # Sort by date
        filtered.sort(key=lambda h: h.date)
        
        return filtered


async def main():
    """Test the Hebcal provider."""
    import asyncio
    
    # Example: New York City coordinates
    provider = HebcalProvider(
        tz_str="America/New_York",
        latitude=40.7128,
        longitude=-74.0060
    )
    
    print("Testing Hebcal Provider\n")
    print("=" * 50)
    
    # Test 1: Get prompt
    print("\n1. Provider Description:")
    print("-" * 50)
    prompt = await provider._get_prompt()
    print(prompt)
    
    # Test 2: Get holidays for current year
    print("\n2. Major holidays in 2026:")
    print("-" * 50)
    holidays = await provider.get_holidays(
        event=None,
        start_year=2026,
        end_year=2026,
        start_month=None,
        end_month=None
    )
    print(holidays)
    
    # Test 3: Search for specific holiday
    print("\n3. Searching for 'Passover' in 2026:")
    print("-" * 50)
    passover = await provider._get_holidays(
        event="Passover",
        start_year=2026,
        end_year=2026,
        start_month=None,
        end_month=None
    )
    print(passover)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
