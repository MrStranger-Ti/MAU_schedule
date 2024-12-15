from rest_framework.viewsets import ModelViewSet

from schedule.api.serializers import InstituteSerializer
from schedule.models import MauInstitute


class InstituteViewSet(ModelViewSet):
    queryset = MauInstitute.objects.all()
    serializer_class = InstituteSerializer
