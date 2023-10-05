from typing import List, Optional
from dataclasses import dataclass
from icalendar import Event
from datetime import datetime
import re

@dataclass
class EventTrigger(object):
    summary_regex: Optional[re.Pattern] = None
    description_regex: Optional[re.Pattern] = None
    trigger: function = lambda:None
    offset: int = 0

@dataclass
class EventStartTrigger(EventTrigger):
    name: str = "Event Start Trigger"
    
    @staticmethod
    def _ical_field():
        return "DTSTART"

@dataclass
class EventEndTrigger(EventTrigger):
    name: str = "Event End Trigger"
    
    @staticmethod
    def _ical_field():
        return "DTEND"

@dataclass
class EventMatch(object):
    ical_event: Event
    event_trigger: EventTrigger
    fire_time: datetime

@dataclass
class Feed(object):
    url: str
    triggers: List[EventTrigger] = []
    refresh_interval: int = 300

    def fetch(self):
