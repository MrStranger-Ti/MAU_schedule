import pytest

from schedule.parser import ParserResponse
from schedule.parser.exceptions import ParserError


class TestParser:
    def test_get_data_success(self, get_parser):
        parser_response = get_parser().get_data()
        assert isinstance(parser_response, ParserResponse)
        assert parser_response.success

    @pytest.mark.parametrize(
        "extra_params",
        [
            {
                "invalid_1": "value_1",
                "invalid_2": "value_2",
            },
            {
                "invalid_1": None,
                "invalid_2": None,
            },
        ],
    )
    def test_validate_extra_data_fail(self, extra_params, mocker, get_parser):
        parser = get_parser()
        spy = mocker.spy(parser, "_validate_extra_data")
        parser._validate_extra_data
        parser.required_extra_data = "required_1", "required_2"
        parser.extra_data = extra_params
        with pytest.raises(ValueError, match="Invalid extra_data."):
            parser.get_data()

        spy.assert_called_once()

    def test_response_is_none_fail(self, get_parser):
        parser = get_parser()
        parser.get_response.return_value = None
        parser_response = parser.get_data()
        assert isinstance(parser_response, ParserResponse)
        assert not parser_response.success
        assert parser_response.error == "Invalid server response."

    def test_status_code_is_not_200(self, get_parser):
        parser = get_parser()
        parser.get_response.return_value.status_code = 400
        parser_response = parser.get_data()
        assert isinstance(parser_response, ParserResponse)
        assert not parser_response.success
        assert parser_response.error == "Invalid server response."

    def test_except(self, get_parser):
        parser = get_parser()
        parser._parse_data.side_effect = ParserError
        parser_response = parser.get_data()
        assert isinstance(parser_response, ParserResponse)
        assert not parser_response.success
        assert parser_response.error == "Parser didn't find any data."
