# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from apps.users.models import CustomUser
# from apps.users.serializers import UserSerializers
# from configs.authentication import HTTPOnlyCookieJWTAuthentication
#
#
# class UserAdminAPIView(
#
#             GenericViewSet,
#             mixins.CreateModelMixin,
#             mixins.ListModelMixin,
#             mixins.RetrieveModelMixin,
#             mixins.UpdateModelMixin,
#             mixins.DestroyModelMixin,
#
#         ):
#
#     permission_classes = [IsAdminUser]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializers
#     lookup_field = 'phone_number'
#
#
# class UserCustomerAPIView(
#
#             GenericViewSet,
#             mixins.CreateModelMixin,
#             mixins.ListModelMixin,
#             mixins.RetrieveModelMixin,
#             mixins.UpdateModelMixin,
#             mixins.DestroyModelMixin,
#
#         ):
#
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     serializer_class = UserSerializers
#     lookup_field = 'phone_number'
#
#     def get_queryset(self):
#
#         return CustomUser.objects.filter(phone_number=self.request.user)
import pprint

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.users.models import CustomUser
from apps.users.serializers import UserSerializers
from configs.authentication import HTTPOnlyCookieJWTAuthentication

@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="لیست تمام کاربران",
        operation_description="این متد تمام کاربران موجود را لیست می‌کند.",
        responses={200: UserSerializers(many=True)}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات کاربر",
        operation_description="این متد اطلاعات کاربری با شماره تلفن مشخص شده را باز می‌گرداند.",
        responses={200: UserSerializers()},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
@method_decorator(name='create', decorator=swagger_auto_schema(
        operation_summary="ایجاد کاربر جدید",
        operation_description="این متد یک کاربر جدید ایجاد می‌کند.",
        request_body=UserSerializers,
        responses={201: UserSerializers()}
    ))
@method_decorator(name='update', decorator=swagger_auto_schema(
        operation_summary="به‌روزرسانی اطلاعات کاربر",
        operation_description="این متد اطلاعات کاربری موجود را به‌روزرسانی می‌کند.",
        request_body=UserSerializers,
        responses={200: UserSerializers()},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
        operation_summary="حذف کاربر",
        operation_description="این متد یک کاربر را بر اساس شماره تلفن حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
class UserAdminAPIView(
            GenericViewSet,
            mixins.CreateModelMixin,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
        ):
    """
    API مدیریت کاربران مخصوص ادمین

    این API به ادمین‌ها اجازه می‌دهد کاربران را ایجاد، مشاهده، ویرایش و حذف کنند.

    پارامترهای ورودی برای متدها:
    - `phone_number`: برای جستجوی کاربر از شماره تلفن استفاده می‌شود (برای متد retrieve و update).
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'phone_number'

    def get_queryset(self):
        return CustomUser.objects.all()


@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_summary="مشاهده حساب کاربری",
        operation_description="این متد اطلاعات پروفایل کاربر لاگین‌شده را برمی‌گرداند.",
        responses={200: UserSerializers()}
    ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_summary="دریافت اطلاعات حساب کاربری",
        operation_description="این متد اطلاعات کاربری لاگین‌شده را بر اساس شماره تلفن برمی‌گرداند.",
        responses={200: UserSerializers()},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
@method_decorator(name='create', decorator=swagger_auto_schema(
        operation_summary="ایجاد حساب کاربری",
        operation_description="این متد امکان ثبت اطلاعات جدید برای کاربر لاگین‌شده را فراهم می‌کند.",
        request_body=UserSerializers,
        responses={201: UserSerializers()}
    ))
@method_decorator(name='update', decorator=swagger_auto_schema(
        operation_summary="به‌روزرسانی اطلاعات حساب کاربری",
        operation_description="این متد اطلاعات پروفایل کاربر لاگین‌شده را به‌روزرسانی می‌کند.",
        request_body=UserSerializers,
        responses={200: UserSerializers()},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
        operation_summary="حذف حساب کاربری",
        operation_description="این متد پروفایل کاربری لاگین‌شده را حذف می‌کند.",
        responses={204: 'حذف موفقیت‌آمیز'},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_PATH, description="شماره تلفن کاربر", type=openapi.TYPE_STRING)
        ]
    ))
class UserCustomerAPIView(
            GenericViewSet,
            mixins.CreateModelMixin,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
        ):
    """
    API مدیریت حساب کاربری برای کاربران لاگین‌شده

    این API به کاربران اجازه می‌دهد پروفایل خود را مشاهده، به‌روزرسانی یا حذف کنند.

    پارامترهای ورودی برای متدها:
    - `phone_number`: برای جستجوی کاربر از شماره تلفن استفاده می‌شود (برای متد retrieve و update).
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    serializer_class = UserSerializers
    lookup_field = 'phone_number'

    def get_queryset(self):
        return CustomUser.objects.filter(phone_number=self.request.user)

