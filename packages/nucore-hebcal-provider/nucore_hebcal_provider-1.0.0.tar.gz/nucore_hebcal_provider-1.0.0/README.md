# NuCore Hebcal Provider Plugin

Jewish holiday provider for NuCore that fetches data from Hebcal API.

## Installation

```bash
pip install nucore-hebcal-provider
```

## Usage

```python
from nucore_hebcal_provider import HebcalHolidayProvider

provider = HebcalHolidayProvider(
    tz_str="America/New_York",
    latitude=40.7128,
    longitude=-74.0060
)

holiday_prompt= await provider.get_holidays(None, start_year=2026, end_year=2028, None, None) 
```

## Features

- Fetches Jewish holidays from Hebcal API
- Includes candle lighting times
- Provides prompt context for holiday-specific rules
- Supports all Hebcal categories (major, minor, modern, etc.)
