select
    m.venue_name    as venue_name,
    m.venue_id      as venue_id,
    m.lon           as lon,
    m.lat           as lat,
    m.event_name    as event_name,
    m.event_id      as event_id,
    m.event_time    as event_time,
    m.event_url     as event_url,
from meetup_events m
group by m.venue_name
