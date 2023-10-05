import requests
from notifical.feed import Feed
from notifical.config import Config

import asyncio

from icalendar import Calendar
from datetime import datetime, timezone
from typing import List

from alert import blink_location

EVENT_LOOP_SPEED = 300 # polling frequency.  Must be > 2*BUFFER
PRE_WARNING = 30 # desired warning before an event in seconds
BUFFER = 20 # This should be at least 2x the time it takes to fetch cal and process

async def sleep_and_fire(seconds, location):
    print(f"Waiting {seconds} seconds")
    await asyncio.sleep(seconds)
    await blink_location(location, color="blue")

async def get_cal(url):
    resp = requests.get(url)
    return Calendar.from_ical(resp.content)



class EventLoop(object):
    def __init__(self, feed: Feed):
        self.url = feed.url

        # Set up triggering events to filter for

    async def run_async(self) -> None:
        last_events_alerted: List[str] = []
        while True:
            ref = datetime.now(timezone.utc)
            results = await asyncio.gather(
                self._schedule_near_events(url, ref, location, last_events_alerted),
                asyncio.sleep(self.feed.refresh_time)
            )
            last_events_alerted = results[0]
    
    async def _schedule_near_events(self, already_alerted):
        cal = self.feed.fetch()
        next_wait = self.feed.refresh_time
        alerted = []

        for event in cal.walk("VEVENT"):
            # times
            event_start = event['DTSTART'].dt
            event_uid = event['UID']
            event_rid = event.get('RECURRENCE-ID','single')
            event_key = f"{event_uid}:{event_rid}"
            delta = event_start - reftime
            s = delta.total_seconds()

            # event is in this search window
            #  fire_and_forget the notification fn
            if PRE_WARNING < s <= EVENT_LOOP_SPEED+PRE_WARNING+BUFFER:
                if event_key in already_alerted:
                    continue
                now = datetime.now(timezone.utc)
                print(f"{now}: Firing for upcoming event")
                until = event_start - now
                asyncio.ensure_future(sleep_and_fire(until.total_seconds()-PRE_WARNING, location))
                alerted.append(event_key)

        return alerted

class Daemon(object):
    def __init__(self, cfg: Config):
        self.loops = [ EventLoop(f) for f in cfg.feeds ]:

    async def run_async(self):
        asyncio.gather(*[l.run_async() for l in self.loops])

    def run(self):
        asyncio.run(self.run_async())


