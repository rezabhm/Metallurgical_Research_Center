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
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.service.serializers import *
from configs.authentication import HTTPOnlyCookieJWTAuthentication

# API برای مدیریت خدمات توسط ادمین
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام خدمات",
        operation_description="این متد تمام خدمات موجود را لیست می‌کند.",
        responses={200: ServiceSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات خدمات",
        operation_description="این متد اطلاعات خدمات مشخص را باز می‌گرداند.",
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='create', decorator=swagger_auto_schema(
        operation_summary="ایجاد خدمت جدید",
        operation_description="این متد یک خدمت جدید ایجاد می‌کند.",
        request_body=ServiceSerializers,
        responses={201: ServiceSerializers()}
    ))
@method_decorator(name='update', decorator=swagger_auto_schema(
        operation_summary="به‌روزرسانی اطلاعات خدمت",
        operation_description="این متد اطلاعات خدمات موجود را به‌روزرسانی می‌کند.",
        request_body=ServiceSerializers,
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
        operation_summary="حذف خدمت",
        operation_description="این متد یک خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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

    def get_queryset(self):
        return Service.objects.all()


# API برای مشاهده خدمات برای عموم
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام خدمات",
        operation_description="این متد تمام خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات خدمات",
        operation_description="این متد اطلاعات خدمات مشخص را برای عموم باز می‌گرداند.",
        responses={200: ServiceSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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

    def get_queryset(self):
        return Service.objects.all()


# API برای مدیریت تصاویر خدمات توسط ادمین
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام تصاویر خدمات",
        operation_description="این متد تمام تصاویر خدمات موجود را لیست می‌کند.",
        responses={200: ServiceImageSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات تصویر خدمات",
        operation_description="این متد اطلاعات تصویر خدمت مشخص را باز می‌گرداند.",
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='create', decorator=swagger_auto_schema(
        operation_summary="ایجاد تصویر خدمت جدید",
        operation_description="این متد یک تصویر جدید برای خدمت ایجاد می‌کند.",
        request_body=ServiceImageSerializers,
        responses={201: ServiceImageSerializers()}
    ))
@method_decorator(name='update', decorator=swagger_auto_schema(
        operation_summary="به‌روزرسانی تصویر خدمت",
        operation_description="این متد اطلاعات تصویر خدمات موجود را به‌روزرسانی می‌کند.",
        request_body=ServiceImageSerializers,
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
        operation_summary="حذف تصویر خدمت",
        operation_description="این متد یک تصویر خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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

    def get_queryset(self):
        return ServiceImage.objects.all()

# API برای مشاهده تصاویر خدمات برای عموم
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام تصاویر خدمات",
        operation_description="این متد تمام تصاویر خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceImageSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات تصویر خدمات",
        operation_description="این متد اطلاعات تصویر خدمت مشخص را برای عموم باز می‌گرداند.",
        responses={200: ServiceImageSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تصویر خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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


# API برای مدیریت تاریخ‌های رزرو خدمات توسط ادمین
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام تاریخ‌های رزرو خدمات",
        operation_description="این متد تمام تاریخ‌های رزرو خدمات موجود را لیست می‌کند.",
        responses={200: ServiceReserveDateSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات تاریخ‌های رزرو خدمات",
        operation_description="این متد اطلاعات تاریخ‌های رزرو خدمات را باز می‌گرداند.",
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='create', decorator=swagger_auto_schema(
        operation_summary="ایجاد تاریخ رزرو خدمت جدید",
        operation_description="این متد یک تاریخ جدید برای رزرو خدمت ایجاد می‌کند.",
        request_body=ServiceReserveDateSerializers,
        responses={201: ServiceReserveDateSerializers()}
    ))
@method_decorator(name='update', decorator=swagger_auto_schema(
        operation_summary="به‌روزرسانی تاریخ رزرو خدمت",
        operation_description="این متد تاریخ رزرو خدمت را به‌روزرسانی می‌کند.",
        request_body=ServiceReserveDateSerializers,
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
        operation_summary="حذف تاریخ رزرو خدمت",
        operation_description="این متد یک تاریخ رزرو خدمت را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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

    def get_queryset(self):
        return ServiceReservedDate.objects.all()


# API برای مشاهده تاریخ‌های رزرو خدمات برای عموم
@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام تاریخ‌های رزرو خدمات",
        operation_description="این متد تمام تاریخ‌های رزرو خدمات موجود را برای عموم لیست می‌کند.",
        responses={200: ServiceReserveDateSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات تاریخ‌های رزرو خدمات",
        operation_description="این متد اطلاعات تاریخ‌های رزرو خدمات را برای عموم باز می‌گرداند.",
        responses={200: ServiceReserveDateSerializers()},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="شناسه تاریخ رزرو خدمات", type=openapi.TYPE_INTEGER)
        ]
    ))
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

    def get_queryset(self):
        return ServiceReservedDate.objects.all()
