import pyparsing as pp

from aa_pbs_exporter.aa_pbs_2020.grammar import (
    FLIGHT,
    FOOTER,
    HEADER_1,
    HEADER_2,
    SEPARATOR,
    SEQ_HEADER,
    SEQ_REPORT,
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
            data = {"footer": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Header_1(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = HEADER_1.parse_string(chunk.text)
            data = {"header_1": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Header_2(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = HEADER_2.parse_string(chunk.text)
            data = {"header_2": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Separator(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = SEPARATOR.parse_string(chunk.text)
            data = {"separator": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class SeqHeader(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = SEQ_HEADER.parse_string(chunk.text)
            data = {"seq_header": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class SeqReport(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = SEQ_REPORT.parse_string(chunk.text)
            data = {"seq_report": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)


class Flight(Parser):
    def parse_chunk(self, context: ParseContext, chunk: Chunk) -> ParseResult:
        try:
            result = FLIGHT.parse_string(chunk.text)
            data = {"flight": result.as_dict()}
            return ParseResult(chunk, self, data)
        except pp.ParseException as ex:
            raise FailedParseException(str(ex), chunk, self, context)
