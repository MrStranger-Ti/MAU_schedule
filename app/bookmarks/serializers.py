from rest_framework.serializers import ModelSerializer

from bookmarks.models import TeacherScheduleBookmark


class BookmarkSerializer(ModelSerializer):
    class Meta:
        model = TeacherScheduleBookmark
        fields = (
            "id",
            "user",
            "teacher_name",
            "teacher_key",
            "created_at",
        )
