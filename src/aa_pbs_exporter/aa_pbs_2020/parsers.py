from typing import Dict

import pyparsing as pp

from aa_pbs_exporter.aa_pbs_2020 import models as pm
from aa_pbs_exporter.aa_pbs_2020.grammar import (
    BASE_EQUIPMENT,
    FLIGHT,
    FOOTER,
    HEADER_1,
    HEADER_2,
    HOTEL,
    RELEASE,
    REPORT,
    SEPARATOR,
    SEQ_HEADER,
    TOTAL,
    TRANSPORTATION,
)
from aa_pbs_exporter.app_lib.chunk_parser import (
    Chunk,
    FailedParseException,
    ParseContext,
    ParseInstruction,
    Parser,
    ParseResult,
    ParseSchema,
)


class Footer(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = FOOTER.parse_string(chunk.text)
            data = pm.Footer(
                issued=result.issued,
                effective=result.effective,
                base=result.base,
                equipment=result.equipment,
                division=result.division,
                internal_page=result.internal_page,
            )
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Header_1(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = HEADER_1.parse_string(chunk.text)
            data: Dict = {}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Header_2(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = HEADER_2.parse_string(chunk.text)
            # print(result.dump())
            data = pm.Header_2(
                calendar_from=result.calendar_from.as_dict(),
                calendar_to=result.calendar_to.as_dict(),
            )
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Separator(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = SEPARATOR.parse_string(chunk.text)
            data: Dict = {}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class SeqHeader(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = SEQ_HEADER.parse_string(chunk.text)
            print(result.dump())
            data = pm.SeqHeader(
                seq_number=result.seq_number,
                ops=result.ops,
                positions=result.positions.as_list(),
            )
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Report(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = REPORT.parse_string(chunk.text)
            data = pm.Report(
                report_local=result.report_local,
                report_home=result.report_home,
                calendar_entries=result.calendar_entries.as_list(),
            )
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Flight(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = FLIGHT.parse_string(chunk.text)
            data = pm.Flight(
                duty_period=result.duty_period,
                day_d=result.day_of_sequence.d,
                day_a=result.day_of_sequence.a,
                equipment_code=result.equipment_code,
                flight_number=result.flight_number,
                departure_city=result.departure_city,
                departure_local=result.departure_local,
                departure_home=result.departure_home,
                crew_meal=result.crew_meal,
                arrival_city=result.arrival_city,
                arrival_local=result.arrival_local,
                arrival_home=result.arrival_home,
                block=result.block,
                total_pay=result.total_pay,
                calendar_entries=result.calendar_entries.as_list(),
            )
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Release(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = RELEASE.parse_string(chunk.text)
            data = {"release": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Hotel(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = HOTEL.parse_string(chunk.text)
            data = {"hotel": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Transportation(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = TRANSPORTATION.parse_string(chunk.text)
            data = {"transportation": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Total(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = TOTAL.parse_string(chunk.text)
            data = {"total": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class BaseEquipment(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = BASE_EQUIPMENT.parse_string(chunk.text)
            data = {"base_equipment": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)
