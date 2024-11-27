from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "pk",
            "user",
            "location",
            "text",
            "expired_date",
        )
