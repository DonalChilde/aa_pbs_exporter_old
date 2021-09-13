from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import List


@dataclass
class Header_2:
    calendar_from: dict = field(default_factory=dict)
    calendar_to: dict = field(default_factory=dict)


@dataclass
class SeqHeader:
    seq_number: int
    ops: int
    positions: List[str] = field(default_factory=list)


@dataclass
class Report:
    report_local: time
    report_home: time
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Flight:
    duty_period: int
    day_d: int
    day_a: int
    equipment_code: int
    flight_number: int
    departure_city: str
    departure_local: time
    departure_home: time
    crew_meal: str
    arrival_city: str
    arrival_local: time
    arrival_home: time
    block: timedelta
    total_pay: timedelta
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Release:
    release_local: time
    release_home: time
    block: timedelta
    synth: timedelta
    total_pay: timedelta
    duty: timedelta
    fdp: timedelta
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Hotel:
    layover_city: str
    hotel: str
    hotel_phone: str
    layover: timedelta
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Transportation:
    transportation: str
    transportation_phone: str
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Total:
    block: timedelta
    synth: timedelta
    total_pay: timedelta
    tafb: timedelta
    calendar_entries: List[str] = field(default_factory=list)


@dataclass
class Footer:
    issued: datetime
    effective: datetime
    base: str
    equipment: str
    division: str
    internal_page: int
