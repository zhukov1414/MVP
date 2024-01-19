from employee.models import CustomUser
from ipr.models import IndividualDevelopmentPlan
from .serializers import (CustomUserListSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          )
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer


class IndividualDevelopmentPlanViewSet(viewsets.ModelViewSet):
    """ВьюСет для создания ИПР."""

    queryset = IndividualDevelopmentPlan.objects.all()
    serializer_class = IndividualDevelopmentPlanCreateSerializer
    #pagination_class = LimitPagePagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IndividualDevelopmentPlanShortSerializer
        return IndividualDevelopmentPlanCreateSerializer