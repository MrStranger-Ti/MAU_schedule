from rest_framework.serializers import ModelSerializer

from teacher_schedule_bookmarks.models import TeacherScheduleBookmark


class TeacherScheduleBookmarkSerializer(ModelSerializer):
    class Meta:
        model = TeacherScheduleBookmark
        fields = "__all__"
        read_only_fields = ["id", "created_at"]
