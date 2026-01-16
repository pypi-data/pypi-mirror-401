from __future__ import annotations
"""
Base class for holiday providers for NuCore.
Provides structures and implementations for:
- Returning a prompt that can be use in nucore to descrive overall holidays
- Fetching holiday data for specific year or events
"""

from abc import ABC,abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class HolidayEvent:
    """Holiday event data structure."""
    date: "datetime.date"
    title: str
    category: str
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    raw: Optional[Dict[str, Any]] = None


class NuCoreHolidayProvider(ABC):
    """Base class for holiday providers."""
    
    def __init__(self, tz_str: str, latitude: float, longitude: float):
        """
            Initialize holiday provider with location and timezone.
        """
        self.tz_str = tz_str
        self.latitude = latitude
        self.longitude = longitude

    async def get_location_info(self):  
        """
            Get location information.
            :returns In english text, describe the location info for the holiday provider.
        """
        return f"Current Location is at latitude {self.latitude}, longitude {self.longitude}, timezone {self.tz_str}."

    async def get_holidays(self, event: str, start_year: int, end_year: int, start_month: int, end_month: int) -> str:
        """
            Subclass: Get holidays given the filters.
            :param event: Event name filter (substring match) - if None, no filter
            :param start_year: Starting year (inclusive) - if None, no filter
            :param end_year: Ending year (inclusive) - if None, no filter
            :param start_month: Starting month (1-12) - if None, no filter
            :param end_month: Ending month (1-12) - if None, no filter
            :return: String description of holidays found to be consumed by NuCore AI.
        """
        holidays = await self._get_holidays(event, start_year, end_year, start_month, end_month)
        if not holidays:
            return "No holidays found for the specified criteria."
        
        result_lines = []
        for holiday in holidays:
            holiday_title = holiday.title if holiday.title else ""
            start_date_str = holiday.start.strftime("%Y-%m-%d") if holiday.start else ""
            end_date_str = holiday.end.strftime("%Y-%m-%d") if holiday.end else ""
            category_str = holiday.category if holiday.category else ""
            holiday_details="" 
            if holiday.raw is not None:
                holiday_details = holiday_details="Details:\n"
                for key, value in holiday.raw.items():
                    holiday_details += f"- {key}: {value}\n"

            line = f"{holiday_title}:\nStart:{start_date_str}\nEnd:{end_date_str}\nCategory:{category_str}\n{holiday_details}"
            result_lines.append(line)
        
        return "\n".join(result_lines)

    @abstractmethod
    async def _get_prompt(self) -> str:
        """
            Descriptive information about this holiday provider
            It must give enough context for the AI to understand what types of holidays
            are provided.  For instance:
            This provider provides U.S. Federal Holidays such as Indpendence Day, Labor Day,
            Thanksgiving, and Christmas. These holidays are widely observed in the United States.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def _get_holidays(self, event: str, start_year: int, end_year: int, start_month: int, end_month: int) -> List[HolidayEvent]:
        """
            Subclass: Get holidays given the filters.
            :param event: Event name filter (substring match) - if None, no filter
            :param start_year: Starting year (inclusive) - if None, no filter
            :param end_year: Ending year (inclusive) - if None, no filter
            :param start_month: Starting month (1-12) - if None, no filter
            :param end_month: Ending month (1-12) - if None, no filter
            :return: List of HolidayEvent objects 
        """
        raise NotImplementedError
    
