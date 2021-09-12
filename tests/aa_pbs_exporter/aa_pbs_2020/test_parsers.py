import datetime

from rich import inspect

from aa_pbs_exporter.aa_pbs_2020.parsers import (
    Flight,
    Footer,
    Header_1,
    Header_2,
    Separator,
    SeqHeader,
    SeqReport,
)
from aa_pbs_exporter.app_lib.chunk_parser import Chunk

TESTDATA = {
    "footer": "COCKPIT  ISSUED 03SEP2021  EFF 01OCT2021               PHX 320  INTL                             PAGE  2205",
    "header_1": "   DAY          --DEPARTURE--    ---ARRIVAL---                GRND/        REST/",
    "header_2": "DP D/A EQ FLT#  STA DLCL/DHBT ML STA ALCL/AHBT  BLOCK  SYNTH   TPAY   DUTY  TAFB   FDP CALENDAR 10/01-10/31",
    "separator": "-----------------------------------------------------------------------------------------------------------",
    "seq_header": "SEQ 8325    1 OPS   POSN CA FO                                                         MO TU WE TH FR SA SU ",
    "seq_report": "                RPT 0600/0600                                                                      -- -- -- ",
    "flight": " 1  1/1 63 2107  PHX 1530/1530    SNA 1653/1653   1.23          0.58                     4 -- -- -- -- -- --",
}


def test_footer():
    grammar = Footer()
    context = None
    chunk = Chunk("foo", TESTDATA["footer"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["footer"]["issue_date"] == datetime.date(2021, 9, 1)


def test_header_1():
    grammar = Header_1()
    context = None
    chunk = Chunk("foo", TESTDATA["header_1"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["header_1"] == {}


def test_header_2():
    grammar = Header_2()
    context = None
    chunk = Chunk("foo", TESTDATA["header_2"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["header_2"]["calendar_from"]["month"] == "10"


def test_separator():
    grammar = Separator()
    context = None
    chunk = Chunk("foo", TESTDATA["separator"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["separator"] == {}


def test_seq_header():
    grammar = SeqHeader()
    context = None
    chunk = Chunk("foo", TESTDATA["seq_header"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["seq_header"]["positions"] == ["CA", "FO"]


def test_seq_report():
    grammar = SeqReport()
    context = None
    chunk = Chunk("foo", TESTDATA["seq_report"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["seq_report"]["local_report"] == datetime.time(6, 0)


def test_flight():
    grammar = Flight()
    context = None
    chunk = Chunk("foo", TESTDATA["flight"])
    result = grammar.parse_chunk(context, chunk)
    inspect(result)
    assert result.data["flight"]["departure_city"] == "PHX"
    assert False
