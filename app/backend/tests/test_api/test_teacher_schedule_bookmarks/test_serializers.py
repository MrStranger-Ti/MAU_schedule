import pytest

from teacher_schedule_bookmarks.serializers import TeacherScheduleBookmarkSerializer
from tests.test_api.test_teacher_schedule_bookmarks.factories import (
    TeacherScheduleBookmarkFactory,
)

pytestmark = pytest.mark.django_db


class TestTeacherScheduleBookmarksSerializer:
    def test_serialize(self, helper):
        bookmark = TeacherScheduleBookmarkFactory().make()
        expected_data = helper.serialize(bookmark)
        serializer = TeacherScheduleBookmarkSerializer(instance=bookmark)

        assert expected_data == serializer.data

    def test_deserialize(self, serialized_bookmark):
        serializer = TeacherScheduleBookmarkSerializer(data=serialized_bookmark)

        assert serializer.is_valid()
        assert not serializer.errors

    @pytest.mark.parametrize("missed_field", ["teacher_name", "teacher_key", "user"])
    def test_deserialize_miss_required_fields(self, missed_field, serialized_bookmark):
        serialized_bookmark.pop(missed_field, None)
        serializer = TeacherScheduleBookmarkSerializer(data=serialized_bookmark)

        assert not serializer.is_valid()
        assert serializer.errors.get(missed_field)
