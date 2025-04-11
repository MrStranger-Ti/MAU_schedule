import pytest

from tests.test_api.test_teacher_schedule_bookmarks.factories import (
    TeacherScheduleBookmarkFactory,
)


@pytest.fixture
def serialized_bookmark(helper):
    bookmark = TeacherScheduleBookmarkFactory(prepare=True).make()
    serialized_data = helper.serialize(bookmark)
    return serialized_data
