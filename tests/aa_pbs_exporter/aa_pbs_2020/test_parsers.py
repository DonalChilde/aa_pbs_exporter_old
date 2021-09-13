import datetime

from rich import inspect

from aa_pbs_exporter.aa_pbs_2020.parsers import (
    BaseEquipment,
    Flight,
    Footer,
    Header_1,
    Header_2,
    Hotel,
    Release,
    Report,
    Separator,
    SeqHeader,
    Total,
    Transportation,
)
from aa_pbs_exporter.app_lib.chunk_parser import Chunk

TESTDATA = {
    "footer": "COCKPIT  ISSUED 03SEP2021  EFF 01OCT2021               PHX 320  INTL                             PAGE  2205",
    "header_1": "   DAY          --DEPARTURE--    ---ARRIVAL---                GRND/        REST/",
    "header_2": "DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 10/01-10/31",
    "separator": "-----------------------------------------------------------------------------------------------------------",
    "seq_header": "SEQ 8325    1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU ",
    "report": "                RPT 0600/0600                                                                      -- -- -- ",
    "flight": " 1  1/1 63 2107  PHX 1530/1530    SNA 1653/1653   1.23          0.58                    -- 04  5 -- -- -- -- --",
    "release": "                                 RLS 2202/2002   7.28   0.00   7.28  11.36       11.06 -- -- -- -- -- -- --",
    "hotel": "                ORD HYATT REGENCY ORD                       18476961234    16.03",
    "hotel_2": "                DFW MARRIOTT DFW AP                         19729298800    13.31       -- -- -- -- -- -- --",
    "hotel_3": "                SEA HOTEL INFO IN CCI/CREW PORTAL                          11.33",
    "transportation": "                    SKYHOP GLOBAL                           9544000412                 25 -- -- -- -- -- 31",
    "total": " TTL                                             21.33   0.00  21.33        73.59",
    "base_equipment": " PHX 320",
}


def test_footer():
    grammar = Footer()
    context = None
    chunk = Chunk("foo", TESTDATA["footer"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data.issued == datetime.date(2021, 9, 1)


def test_header_1():
    grammar = Header_1()
    context = None
    chunk = Chunk("foo", TESTDATA["header_1"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data == {}


def test_header_2():
    grammar = Header_2()
    context = None
    chunk = Chunk("foo", TESTDATA["header_2"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data.calendar_from["month"] == 10


def test_separator():
    grammar = Separator()
    context = None
    chunk = Chunk("foo", TESTDATA["separator"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data == {}


def test_seq_header():
    grammar = SeqHeader()
    context = None
    chunk = Chunk("foo", TESTDATA["seq_header"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data.positions == ["CA", "FO"]


def test_report():
    grammar = Report()
    context = None
    chunk = Chunk("foo", TESTDATA["report"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data.report_local == datetime.time(6, 0)


def test_flight():
    grammar = Flight()
    context = None
    chunk = Chunk("foo", TESTDATA["flight"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data.departure_city == "PHX"
    assert False


def test_release():
    grammar = Release()
    context = None
    chunk = Chunk("foo", TESTDATA["release"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["release"]["release_local"] == datetime.time(22, 2)
    # assert False


def test_hotel():
    grammar = Hotel()
    context = None
    chunk = Chunk("foo", TESTDATA["hotel"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["hotel"]["layover_city"] == "ORD"
    # assert False


def test_transportation():
    grammar = Transportation()
    context = None
    chunk = Chunk("foo", TESTDATA["transportation"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["transportation"]["transportation"] == "SKYHOP GLOBAL"
    # assert False


def test_total():
    grammar = Total()
    context = None
    chunk = Chunk("foo", TESTDATA["total"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["total"]["block"] == datetime.timedelta(seconds=77580)
    # assert False


def test_base_equipment():
    grammar = BaseEquipment()
    context = None
    chunk = Chunk("foo", TESTDATA["base_equipment"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["base_equipment"]["base"] == "PHX"
    # assert False
