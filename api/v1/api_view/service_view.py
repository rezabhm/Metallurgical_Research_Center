# from rest_framework.permissions import AllowAny, IsAdminUser
# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from apps.service.serializers import *
# from configs.authentication import HTTPOnlyCookieJWTAuthentication
#
#
# class ServiceAdminAPIView(
#
#         GenericViewSet,
#         mixins.CreateModelMixin,
#         mixins.ListModelMixin,
#         mixins.UpdateModelMixin,
#         mixins.RetrieveModelMixin,
#         mixins.DestroyModelMixin,
#
#     ):
#
#     permission_classes = [IsAdminUser]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializers
#
#
# class ServiceAnyAPIView(
#
#         GenericViewSet,
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#
#     ):
#
#     permission_classes = [AllowAny]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializers
#
#
# class ServiceImageAdminAPIView(
#
#         GenericViewSet,
#         mixins.CreateModelMixin,
#         mixins.ListModelMixin,
#         mixins.UpdateModelMixin,
#         mixins.RetrieveModelMixin,
#         mixins.DestroyModelMixin,
#
#     ):
#
#     permission_classes = [IsAdminUser]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = ServiceImage.objects.all()
#     serializer_class = ServiceImageSerializers
#
#
# class ServiceImageAnyAPIView(
#
#         GenericViewSet,
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#
#     ):
#
#     permission_classes = [AllowAny]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = ServiceImage.objects.all()
#     serializer_class = ServiceImageSerializers
#
#
# class ServiceReserveDateAdminAPIView(
#
#         GenericViewSet,
#         mixins.CreateModelMixin,
#         mixins.ListModelMixin,
#         mixins.UpdateModelMixin,
#         mixins.RetrieveModelMixin,
#         mixins.DestroyModelMixin,
#
#     ):
#
#     permission_classes = [IsAdminUser]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = ServiceReservedDate.objects.all()
#     serializer_class = ServiceReserveDateSerializers
#
#
# class ServiceReserveDateAnyAPIView(
#
#         GenericViewSet,
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#
#     ):
#
#     permission_classes = [AllowAny]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = ServiceReservedDate.objects.all()
#     serializer_class = ServiceReserveDateSerializers
#
#

from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.service.serializers import *
from configs.authentication import HTTPOnlyCookieJWTAuthentication

# API برای مدیریت خدمات توسط ادمین
class ServiceAdminAPIView(
        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
    ):
    """
    API مدیریت خدمات مخصوص ادمین

    این API به ادمین‌ها اجازه می‌دهد خدمات را ایجاد، مشاهده، ویرایش و حذف کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست مگر برای جستجو.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام خدمات",
        operation_description="این متد تمام خدمات موجود را لیست می‌کند.",
        responses={200: ServiceSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات خدمات",
        operation_description="این متد اطلاعات خدمات مشخص را باز می‌گرداند.",
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد خدمت جدید",
        operation_description="این متد یک خدمت جدید ایجاد می‌کند.",
        request_body=ServiceSerializers,
        responses={201: ServiceSerializers()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی اطلاعات خدمت",
        operation_description="این متد اطلاعات خدمات موجود را به‌روزرسانی می‌کند.",
        request_body=ServiceSerializers,
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف خدمت",
        operation_description="این متد یک خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# API برای مشاهده خدمات برای عموم
class ServiceAnyAPIView(
        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
    ):
    """
    API مشاهده خدمات برای عموم

    این API به عموم اجازه می‌دهد تا خدمات را مشاهده کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام خدمات",
        operation_description="این متد تمام خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات خدمات",
        operation_description="این متد اطلاعات خدمات مشخص را برای عموم باز می‌گرداند.",
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# API برای مدیریت تصاویر خدمات توسط ادمین
class ServiceImageAdminAPIView(
        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
    ):
    """
    API مدیریت تصاویر خدمات مخصوص ادمین

    این API به ادمین‌ها اجازه می‌دهد تصاویر خدمات را ایجاد، مشاهده، ویرایش و حذف کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست مگر برای جستجو.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام تصاویر خدمات",
        operation_description="این متد تمام تصاویر خدمات موجود را لیست می‌کند.",
        responses={200: ServiceImageSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات تصویر خدمات",
        operation_description="این متد اطلاعات تصویر خدمت مشخص را باز می‌گرداند.",
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد تصویر خدمت جدید",
        operation_description="این متد یک تصویر جدید برای خدمت ایجاد می‌کند.",
        request_body=ServiceImageSerializers,
        responses={201: ServiceImageSerializers()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی تصویر خدمت",
        operation_description="این متد اطلاعات تصویر خدمات موجود را به‌روزرسانی می‌کند.",
        request_body=ServiceImageSerializers,
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف تصویر خدمت",
        operation_description="این متد یک تصویر خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# API برای مشاهده تصاویر خدمات برای عموم
class ServiceImageAnyAPIView(
        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
    ):
    """
    API مشاهده تصاویر خدمات برای عموم

    این API به عموم اجازه می‌دهد تا تصاویر خدمات را مشاهده کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام تصاویر خدمات",
        operation_description="این متد تمام تصاویر خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceImageSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات تصویر خدمات",
        operation_description="این متد اطلاعات تصویر خدمت مشخص را برای عموم باز می‌گرداند.",
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# API برای مدیریت تاریخ‌های رزرو خدمات توسط ادمین
class ServiceReserveDateAdminAPIView(
        GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
    ):
    """
    API مدیریت تاریخ‌های رزرو خدمات مخصوص ادمین

    این API به ادمین‌ها اجازه می‌دهد تاریخ‌های رزرو خدمات را ایجاد، مشاهده، ویرایش و حذف کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست مگر برای جستجو.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    queryset = ServiceReservedDate.objects.all()
    serializer_class = ServiceReserveDateSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام تاریخ‌های رزرو خدمات",
        operation_description="این متد تمام تاریخ‌های رزرو خدمات موجود را لیست می‌کند.",
        responses={200: ServiceReserveDateSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات تاریخ‌های رزرو خدمات",
        operation_description="این متد اطلاعات تاریخ‌های رزرو خدمات را باز می‌گرداند.",
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد تاریخ رزرو خدمت جدید",
        operation_description="این متد یک تاریخ جدید برای رزرو خدمت ایجاد می‌کند.",
        request_body=ServiceReserveDateSerializers,
        responses={201: ServiceReserveDateSerializers()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی تاریخ رزرو خدمت",
        operation_description="این متد تاریخ رزرو خدمت را به‌روزرسانی می‌کند.",
        request_body=ServiceReserveDateSerializers,
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف تاریخ رزرو خدمت",
        operation_description="این متد یک تاریخ رزرو خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# API برای مشاهده تاریخ‌های رزرو خدمات برای عموم
class ServiceReserveDateAnyAPIView(
        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
    ):
    """
    API مشاهده تاریخ‌های رزرو خدمات برای عموم

    این API به عموم اجازه می‌دهد تا تاریخ‌های رزرو خدمات را مشاهده کنند.

    پارامترهای ورودی برای متدها:
    - هیچ پارامتر ورودی در متدهای این API لازم نیست.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = ServiceReservedDate.objects.all()
    serializer_class = ServiceReserveDateSerializers

    @swagger_auto_schema(
        operation_summary="لیست تمام تاریخ‌های رزرو خدمات",
        operation_description="این متد تمام تاریخ‌های رزرو خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceReserveDateSerializers(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات تاریخ‌های رزرو خدمات",
        operation_description="این متد اطلاعات تاریخ‌های رزرو خدمات را برای عموم باز می‌گرداند.",
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
