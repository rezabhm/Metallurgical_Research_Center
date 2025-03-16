from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.service.serializers import *


class ServiceAdminAPIView(

        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,

    ):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers


class ServiceAnyAPIView(

        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,

    ):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers


class ServiceImageAdminAPIView(

        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,

    ):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializers


class ServiceImageAnyAPIView(

        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,

    ):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializers


class ServiceReserveDateAdminAPIView(

        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,

    ):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = ServiceReservedDate.objects.all()
    serializer_class = ServiceReserveDateSerializers


class ServiceReserveDateAnyAPIView(

        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,

    ):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    queryset = ServiceReservedDate.objects.all()
    serializer_class = ServiceReserveDateSerializers


