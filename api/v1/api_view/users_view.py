from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.models import CustomUser
from apps.users.serializers import UserSerializers


class UserAdminAPIView(

            GenericViewSet,
            mixins.CreateModelMixin,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,

        ):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'phone_number'


class UserCustomerAPIView(

            GenericViewSet,
            mixins.CreateModelMixin,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,

        ):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializers
    lookup_field = 'phone_number'

    def get_queryset(self):

        return CustomUser.objects.filter(phone_number=self.request.user)
