from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.blog.document import *
from apps.blog.serializers import *


class CategoryAPIView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializers
    queryset = Category.objects()


class BlogAPiView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogSerializers
    queryset = Blog.objects()


class BlogImageAPiView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogImageSerializers
    queryset = BlogImage.objects()


class BlogContentAPiView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogContentSerializers
    queryset = BlogContent.objects()


class CategoryReadAPIView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CategorySerializers
    queryset = Category.objects()


class BlogReadAPiView(

    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,

    ):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = BlogSerializers
    queryset = Blog.objects()
