from rest_framework import serializers

from schedule.models import MauInstitute


class MauInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MauInstitute
        fields = "__all__"
        read_only_fields = ["id"]
