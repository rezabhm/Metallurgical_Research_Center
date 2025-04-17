# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
#
# from apps.users.serializers import OTPVerifyCodeSerializers
# from apps.users.service import check_user_exist, create_user
# from utils.sms import send_password_code_sms
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
#
#
# class OTPSendCodeAPIView(GenericAPIView):
#
#     authentication_classes = []
#     permission_classes = [AllowAny]
#
#     def get(self, request, **kwargs):
#
#         # get user
#         user = check_user_exist(kwargs.get('phone_number'))
#
#         # check user exist or we must create new user
#         if user:
#             user.generate_otp_code()
#
#         else:
#             user = create_user(phone_number=kwargs.get('phone_number'))
#             user.generate_otp_code()
#         send_password_code_sms(user.phone_number, user.otp_code)
#         return JsonResponse(data={'message': 'code successfully sent'}, status=status.HTTP_200_OK)
#
#
# class OTPVerifyCodeAPIView(GenericAPIView):
#
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = OTPVerifyCodeSerializers
#
#     def post(self, request, **kwargs):
#
#         # get user
#         user = check_user_exist(phone_number=kwargs.get('phone_number'))
#
#         # check user exist or not ( if user didn't exist we must return 404 error response )
#         if user:
#
#             otp_verify_status = user.verify_otp_code(request.data.get('code'))
#
#             if otp_verify_status in [-1, 0]:
#                 return JsonResponse(data={
#
#                     'message': 'You have exceeded the time limit.' if otp_verify_status == -1 else 'wrong code'
#
#                 }, status=status.HTTP_400_BAD_REQUEST)
#
#             else:
#
#                 refresh = RefreshToken.for_user(user)
#                 access = refresh.access_token
#
#                 # Response
#                 response = JsonResponse({
#                     'is_signup': user.is_signup,
#                 }, status=status.HTTP_200_OK)
#
#                 # تنظیم HttpOnly cookie
#                 response.set_cookie(
#                     key='access_token',
#                     value=str(access),
#                     httponly=True,
#                     secure=True,  # فقط در حالت HTTPS فعال باشه
#                     samesite='Lax',  # یا 'Strict' / 'None' بسته به نیاز
#                     max_age=60 * 60 * 24  # مدت زمان اعتبار access token (اینجا 1 روز)
#                 )
#
#                 response.set_cookie(
#                     key='refresh_token',
#                     value=str(refresh),
#                     httponly=True,
#                     secure=True,
#                     samesite='Lax',
#                     max_age=60 * 60 * 24 * 30
#                 )
#
#         else:
#
#             return JsonResponse(data={'message': "user didn't exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
# class LogoutAPIView(APIView):
#     def post(self, request):
#         response = Response({'message': 'logged out'}, status=status.HTTP_200_OK)
#
#         # get refresh token from cookies
#         refresh_token = request.COOKIES.get('refresh_token')
#         if refresh_token:
#             try:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()  # ⛔️ Expire the token!
#             except TokenError:
#                 pass  # توکن نامعتبر بود، مشکلی نیست
#
#         # delete the cookies
#         response.delete_cookie('access_token')
#         response.delete_cookie('refresh_token')
#
#         return response
#
#
# class RefreshTokenCookieAPIView(APIView):
#     def post(self, request):
#         refresh_token = request.COOKIES.get('refresh_token')
#
#         if not refresh_token:
#             return Response({'error': 'Refresh token not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         try:
#             # validate refresh token
#             refresh = RefreshToken(refresh_token)
#
#             # اختیاری: بلاک‌لیست کردن توکن قبلی
#             try:
#                 refresh.blacklist()
#             except AttributeError:
#                 # اگه blacklist فعال نباشه، ارور نده
#                 pass
#
#             # ساختن توکن جدید
#             new_refresh = RefreshToken.for_user(refresh.user)
#             new_access = new_refresh.access_token
#
#             # ساخت response
#             response = Response({'message': 'Token refreshed successfully'}, status=status.HTTP_200_OK)
#
#             # ست کردن کوکی‌ها
#             response.set_cookie(
#                 key='access_token',
#                 value=str(new_access),
#                 httponly=True,
#                 secure=True,
#                 samesite='Lax',
#                 max_age=60 * 60 * 24  # 1 روز
#             )
#
#             response.set_cookie(
#                 key='refresh_token',
#                 value=str(new_refresh),
#                 httponly=True,
#                 secure=True,
#                 samesite='Lax',
#                 max_age=60 * 60 * 24 * 30  # 30 روز
#             )
#
#             return response
#
#         except TokenError:
#             return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
#
import pprint

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import OTPVerifyCodeSerializers
from apps.users.service import check_user_exist, create_user
from utils.sms import send_password_code_sms
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class OTPSendCodeAPIView(GenericAPIView):
    """
    این API برای ارسال کد تایید (OTP) به شماره تلفن کاربر استفاده می‌شود.
    اگر کاربر قبلاً در سیستم ثبت‌نام کرده باشد، کد OTP برای او ارسال می‌شود،
    و اگر کاربری با شماره تلفن داده شده وجود نداشته باشد، یک کاربر جدید ایجاد می‌شود و کد OTP برای او ارسال می‌گردد.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        """
        ارسال کد OTP به شماره تلفن کاربر
        """
        # بررسی وجود کاربر
        user = check_user_exist(kwargs.get('phone_number'))

        # اگر کاربر وجود دارد، کد OTP جدید تولید می‌شود
        if user:
            user.generate_otp_code()

        else:
            # اگر کاربر وجود ندارد، یک کاربر جدید ایجاد می‌شود
            user = create_user(phone_number=kwargs.get('phone_number'))
            user.generate_otp_code()

        # ارسال کد OTP از طریق SMS
        send_password_code_sms(user.phone_number, user.otp_code)

        return JsonResponse(data={'message': 'کد با موفقیت ارسال شد'}, status=status.HTTP_200_OK)


class OTPVerifyCodeAPIView(GenericAPIView):
    """
    این API برای تایید کد OTP ارسال شده به کاربر استفاده می‌شود.
    اگر کد OTP صحیح باشد و در زمان معتبر وارد شود، کاربر می‌تواند وارد سیستم شود.
    در غیر این صورت، یک پیام خطا ارسال می‌شود.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = OTPVerifyCodeSerializers

    def post(self, request, **kwargs):
        """
        تایید کد OTP و ارسال توکن دسترسی (Access Token) در صورت تایید موفقیت‌آمیز
        """
        # بررسی وجود کاربر
        user = check_user_exist(phone_number=kwargs.get('phone_number'))

        # بررسی اینکه آیا کاربر وجود دارد یا خیر
        if user:

            # بررسی وضعیت تایید کد OTP
            otp_verify_status = user.verify_otp_code(request.data.get('code'))

            if otp_verify_status in [-1, 0]:
                return JsonResponse(data={
                    'message': 'زمان مجاز برای وارد کردن کد تمام شده است.' if otp_verify_status == -1 else 'کد اشتباه است.'
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                # تولید توکن‌های refresh و access
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                # ساخت پاسخ
                response = JsonResponse({
                    'is_signup': user.is_signup,
                }, status=status.HTTP_200_OK)

                # تنظیم HttpOnly cookie برای توکن دسترسی
                response.set_cookie(
                    key='access_token',
                    value=str(access),
                    httponly=True,
                    secure=False,  # فقط در حالت HTTPS فعال باشد
                    samesite='Lax',  # یا 'Strict' / 'None' بسته به نیاز
                    max_age=60 * 60 * 24*30 # مدت زمان اعتبار توکن (1 روز)
                )

                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=60 * 60 * 24 * 30  # مدت زمان اعتبار توکن refresh (30 روز)
                )
                return response

        else:
            return JsonResponse(data={'message': "کاربر وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    """
    این API برای خروج کاربر از سیستم و حذف توکن‌ها از مرورگر استفاده می‌شود.
    """

    def post(self, request):
        """
        خروج کاربر از سیستم و حذف توکن‌ها از کوکی‌ها
        """
        response = Response({'message': 'خروج انجام شد'}, status=status.HTTP_200_OK)

        # دریافت توکن refresh از کوکی‌ها
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                # غیر فعال کردن توکن refresh
                token = RefreshToken(refresh_token)
                token.blacklist()  # منقضی کردن توکن
            except TokenError:
                pass  # اگر توکن معتبر نبود، هیچ مشکلی نیست

        # حذف کوکی‌ها
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class RefreshTokenCookieAPIView(APIView):
    """
    این API برای بروزرسانی توکن‌های دسترسی و refresh استفاده می‌شود.
    اگر توکن refresh منقضی نشده باشد، توکن جدید برای کاربر صادر می‌شود.
    """

    def get(self, request):
        """
        بروزرسانی توکن‌های دسترسی و refresh
        """
        # دریافت توکن refresh از کوکی‌ها
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'توکن refresh در کوکی‌ها پیدا نشد'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # اعتبارسنجی توکن refresh
            refresh = RefreshToken(refresh_token)

            # اختیاری: بلاک‌لیست کردن توکن قبلی
            try:
                refresh.blacklist()
            except AttributeError:
                # اگر blacklist فعال نباشد، ارور ندهد
                pass

            # ایجاد توکن جدید
            usr = CustomUser.objects.get(id=refresh['user_id'])
            new_refresh = RefreshToken.for_user(usr)
            new_access = new_refresh.access_token

            # ساخت پاسخ
            response = Response({'message': 'توکن با موفقیت بروزرسانی شد'}, status=status.HTTP_200_OK)

            # تنظیم کوکی‌ها
            response.set_cookie(
                key='access_token',
                value=str(new_access),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=1000 * 60 * 60 * 24,  # 1 روز
                path='/'
            )

            response.set_cookie(
                key='refresh_token',
                value=str(new_refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=1000 * 60 * 60 * 24 * 30,  # 30 روز
                path='/'
            )

            return response

        except TokenError:
            return Response({'error': 'توکن refresh نامعتبر یا منقضی شده است'}, status=status.HTTP_401_UNAUTHORIZED)
