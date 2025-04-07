import pytest

from schedule.parser import ParserResponse


class TestParserResponse:
    def test_success_response(self):
        parser_response = ParserResponse(data="some_data")
        assert parser_response.success

    def test_data_is_none(self):
        parser_response = ParserResponse()
        assert not parser_response.success

    @pytest.mark.parametrize("error", ["some error", ValueError("some error")])
    def test_error_passed(self, error):
        parser_response = ParserResponse(error=error)
        assert not parser_response.success
        assert parser_response.error == "some error"
