from datetime import date, datetime, timedelta

import pyparsing as pp

from aa_pbs_exporter.app_lib.datetime_util import string_to_date

"""
COCKPIT  ISSUED 03SEP2021  EFF 01OCT2021               PHX 320  INTL                             PAGE  2205
"""


def short_string_to_date(s: str, loc: int, tocs: pp.ParseResults):
    return string_to_date(tocs[0][0], "%m%b%Y")


def string_to_time(s: str, loc: int, tocs: pp.ParseResults):
    return datetime.strptime(tocs[0], "%H%M").time()


def duration_to_timedelta(s: str, loc: int, tocs: pp.ParseResults):
    print(tocs.dump())
    return timedelta(hours=int(tocs[0]["hours"]), minutes=int(tocs[0]["minutes"]))


DAY_NUMERAL = pp.Word(pp.nums, exact=2)("day")
SHORT_MONTH = pp.Word(pp.alphas, exact=3)("month")
MONTH_NUMERAL = pp.Word(pp.nums, exact=2)("month")
YEAR = pp.Word(pp.nums, exact=4)("year")
DATE = pp.Combine(DAY_NUMERAL + SHORT_MONTH + YEAR).set_parse_action(
    short_string_to_date
)
TIME = pp.Combine(pp.Word(pp.nums, exact=2) + pp.Word(pp.nums, exact=2)).setParseAction(
    string_to_time
)
MONTH_DAY = MONTH_NUMERAL + "/" + DAY_NUMERAL
BASE = pp.Word(pp.alphas, exact=3)("base")
EQUIPMENT = pp.Word(pp.nums, exact=3)("equipment")
DIVISION = pp.Literal("INTL") | pp.Literal("DOM")
SEQ_NUMBER = pp.Word(pp.nums, min=1)("seq_number")
OPS = pp.Word(pp.nums, min=1)("ops")
POSITIONS = pp.one_of("CA FO", as_keyword=True)
CALENDAR_HEADER = pp.Literal("MO") + "TU" + "WE" + "TH" + "FR" + "SA" + "SU"
CALENDAR_ENTRY = pp.Word("-", exact=2, as_keyword=True) | pp.Word(
    pp.nums, as_keyword=True
)
DUTY_PERIOD = pp.Word(pp.nums, exact=1)("duty_period")
EQUIPMENT_CODE = pp.Word(pp.nums, exact=2, as_keyword=True)
DAY_OF_SEQUENCE = pp.Group(
    pp.Word(pp.nums, exact=1)("d") + "/" + pp.Word(pp.nums, exact=1)("a")
)("day_of_sequence")
FLIGHT_NUMBER = pp.Word(pp.nums, as_keyword=True)("flight_number")
CITY_CODE = pp.Word(pp.alphas, exact=3, as_keyword=True)
CREW_MEAL = pp.Word("BLD", exact=1, as_keyword=True)
DURATION = pp.Combine(
    pp.Word(pp.nums, min=1)("hours") + "." + pp.Word(pp.nums, exact=2)("minutes")
).set_parse_action(duration_to_timedelta)
# COCKPIT  ISSUED 03SEP2021  EFF 01OCT2021               PHX 320  INTL                             PAGE  2205
FOOTER = (
    pp.StringStart()
    + "COCKPIT"
    + "ISSUED"
    + DATE("issue_date")
    + "EFF"
    + DATE("effective_date")
    + BASE
    + EQUIPMENT
    + DIVISION("division")
    + "PAGE"
    + pp.Word(pp.nums)("internal_page_no")
    + pp.StringEnd()
)
#   DAY          --DEPARTURE--    ---ARRIVAL---                GRND/        REST/
HEADER_1 = (
    pp.StringStart()
    + "DAY"
    + "--DEPARTURE--"
    + "---ARRIVAL---"
    + "GRND/"
    + "REST/"
    + pp.StringEnd()
)
# DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 10/01-10/31
HEADER_2 = (
    pp.StringStart()
    + "DP"
    + "D/A"
    + "EQ"
    + "FLT#"
    + "STA"
    + "DLCL/DHBT"
    + "ML"
    + "STA"
    + "ALCL/AHBT"
    + "BLOCK"
    + "SYNTH"
    + "TPAY"
    + "DUTY"
    + "TAFB"
    + "FDP"
    + "CALENDAR"
    + pp.Group(MONTH_DAY)("calendar_from")
    + "-"
    + pp.Group(MONTH_DAY)("calendar_to")
    + pp.StringEnd()
)
# -----------------------------------------------------------------------------------------------------------
SEPARATOR = pp.StringStart() + pp.Word("-", min=5) + pp.StringEnd()
# SEQ 8325    1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU
SEQ_HEADER = (
    pp.StringStart()
    + "SEQ"
    + SEQ_NUMBER
    + OPS
    + "OPS"
    + "POSN"
    + pp.OneOrMore(POSITIONS)("positions")
    + CALENDAR_HEADER
    + pp.StringEnd()
)
#                RPT 0600/0600                                                                      -- -- --
SEQ_REPORT = (
    pp.StringStart()
    + "RPT"
    + TIME("report_local")
    + "/"
    + TIME("report_home")
    + pp.ZeroOrMore(CALENDAR_ENTRY)("calendar_entries")
    + pp.StringEnd()
)
# 1  1/1 63 2107  PHX 1530/1530    SNA 1653/1653   1.23          0.58                     4 -- -- -- -- -- --
FLIGHT = (
    pp.StringStart()
    + DUTY_PERIOD
    + DAY_OF_SEQUENCE
    + EQUIPMENT_CODE
    + FLIGHT_NUMBER
    + CITY_CODE("departure_city")
    + TIME("departure_local")
    + "/"
    + TIME("departure_home")
    + pp.Opt(CREW_MEAL, default=None)("crew_meal")
    + CITY_CODE("arrival_city")
    + TIME("arrival_local")
    + "/"
    + TIME("arrival_home")
    + DURATION("block")
    + DURATION("total_pay")
    + pp.ZeroOrMore(CALENDAR_ENTRY)("calendar_entries")
    + pp.StringEnd()
)
