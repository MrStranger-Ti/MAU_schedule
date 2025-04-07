class TestScheduleParser:
    def test_get_cache_key(self, get_schedule_parser):
        cache_key = "test_key"
        parser = get_schedule_parser(unique_key=cache_key)
        expected_key = (
            parser.base_key
            + "_"
            + cache_key
            + f"_period_{parser.period_manager.period}"
        )
        assert expected_key == parser.get_cache_key()

    def test_periods_params_set(self, get_schedule_parser):
        parser = get_schedule_parser()
        expected_params = {
            "perstart": parser.period_manager.start,
            "perend": parser.period_manager.end,
        }
        for param_name, value in expected_params.items():
            parser_params = parser.params
            assert param_name in parser_params
            assert value == parser_params[param_name]
