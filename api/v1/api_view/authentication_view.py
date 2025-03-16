from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import OTPVerifyCodeSerializers
from apps.users.service import check_user_exist, create_user
from utils.sms import send_password_code_sms


class OTPSendCodeAPIView(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):

        # get user
        user = check_user_exist(kwargs.get('phone_number'))

        # check user exist or we must create new user
        if user:
            user.generate_otp_code()

        else:
            user = create_user(phone_number=kwargs.get('phone_number'))
            user.generate_otp_code()
        send_password_code_sms(user.phone_number, user.otp_code)
        return JsonResponse(data={'message': 'code successfully sent'}, status=status.HTTP_200_OK)


class OTPVerifyCodeAPIView(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = OTPVerifyCodeSerializers

    def post(self, request, **kwargs):

        # get user
        user = check_user_exist(phone_number=kwargs.get('phone_number'))

        # check user exist or not ( if user didn't exist we must return 404 error response )
        if user:

            otp_verify_status = user.verify_otp_code(request.POST.get('code'))
            if otp_verify_status in [-1, 0]:
                return JsonResponse(data={

                    'message': 'You have exceeded the time limit.' if otp_verify_status == -1 else 'wrong code'

                }, status=status.HTTP_400_BAD_REQUEST)

            else:

                refresh = RefreshToken.for_user(user)
                return JsonResponse(data={

                    'refresh-token': str(refresh),
                    'access-token': str(refresh.access_token),
                    'is_signup': user.is_signup,

                }, status=status.HTTP_200_OK)

        else:

            return JsonResponse(data={'message': "user didn't exist"}, status=status.HTTP_404_NOT_FOUND)
