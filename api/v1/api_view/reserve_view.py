# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from apps.reserve.document import ServiceReserve
# from apps.reserve.serializers import ServiceReserveSerializers
# from apps.users.models import CustomUser
# from configs.authentication import HTTPOnlyCookieJWTAuthentication
#
#
# class ReserveAPIView(GenericAPIView):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = ServiceReserveSerializers
#
#     def get(self, request):
#         """ گرفتن اطلاعات یک رزرو بر اساس , باید reserve-id (string) در لینک ها ارسال شود """
#
#         reserve_id = request.query_params.get('reserve-id')
#
#         if not reserve_id:
#             return JsonResponse({'message': 'reserve-id is required in links query params'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         reserve_obj = ServiceReserve.objects(id=reserve_id).first()
#         if not reserve_obj:
#             return JsonResponse({'message': 'reserve-id does not match'}, status=status.HTTP_404_NOT_FOUND)
#
#         is_admin = request.user.role == 'admin'
#         if not is_admin and reserve_obj.user != request.user.phone_number:
#             return JsonResponse({'message':
#                                  'you can not access to this reserve'},
#                                 status=status.HTTP_403_FORBIDDEN)
#
#         reserver_serializer = self.serializer_class(reserve_obj)
#         return JsonResponse(reserver_serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         """ ایجاد یک رزرو جدید  با پارامتر های user
#         , در صورتی که ادمین باشد باید شماره موبایل کاربر با کلید user در دیتا ارسال شود در غیر این صورت داده ها باید خالی ارسال شود"""
#
#         is_admin = request.user.role == 'admin'
#         phone_number = request.data.get('user') if is_admin else request.user.phone_number
#
#         if is_admin and not phone_number:
#             return JsonResponse({'message':
#                                  'User phone number is required for admins , send it with name (user) in post data'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         user = CustomUser.objects.filter(phone_number=phone_number).first()
#         if not user:
#             return JsonResponse({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
#
#         reserve_obj = ServiceReserve(user=user.phone_number)
#         reserve_obj.save()
#
#         reserve_serializer = self.serializer_class(reserve_obj)
#         return JsonResponse(reserve_serializer.data, status=status.HTTP_201_CREATED)
#
#     def patch(self, request):
#         """ به‌روزرسانی مرحله‌ی رزرو ,
#          باید پارامتر های reserve-id (string) , next-stage (boolean) را در لینک خود وارد نمایید """
#
#         is_admin = request.user.role == 'admin'
#         reserve_id = request.query_params.get('reserve-id')
#
#         if not reserve_id:
#             return JsonResponse({'message': 'reserve-id is required in links query params'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         reserve = ServiceReserve.objects(id=reserve_id).first()
#         if not reserve:
#             return JsonResponse({'message': 'reserve id not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         if not is_admin and request.user.phone_number != reserve.user:
#             return JsonResponse({'message': 'You do not have access to this reserve'}, status=status.HTTP_403_FORBIDDEN)
#
#         next_stage_status = request.query_params.get('next-stage')
#         if not next_stage_status:
#             return JsonResponse(data={'message': "next-stage require in links query params"})
#
#         if next_stage_status:
#             if reserve.stage not in [1, 2, 3, 4, 5]:
#                 return JsonResponse({'message': "wrong stage number, acceptable stages: [1,2,3,4,5]"},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             update_status, update_message = reserve.handle_next_stage(request.data)
#         else:
#             if reserve.stage not in [2, 3, 4]:
#                 return JsonResponse({'message': "wrong stage number, acceptable stages: [2,3,4]"},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             update_status, update_message = reserve.handle_previous_stage(request.data)
#
#         return JsonResponse(update_message, status=status.HTTP_200_OK if update_status else status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         """ کنسل رزرو , باید reserve-id (string) را در لینک وارد نمایید"""
#
#         is_admin = request.user.role == 'admin'
#         reserve_id = request.query_params.get('reserve-id')
#
#         if not reserve_id:
#             return JsonResponse({'message': 'reserve-id is required in links query params'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         reserve = ServiceReserve.objects(id=reserve_id).first()
#         if not reserve:
#             return JsonResponse({'message': 'reserve id not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         if not is_admin and request.user.phone_number != reserve.user:
#             return JsonResponse({'message': 'You do not have access to this reserve'},
#                                 status=status.HTTP_403_FORBIDDEN)
#
#         reserve.cancel_reservation()
#
#         return JsonResponse({'message': "successfully canceled reserve"}, status=status.HTTP_200_OK)

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.reserve.document import ServiceReserve
from apps.reserve.serializers import ServiceReserveSerializers
from apps.users.models import CustomUser
from configs.authentication import HTTPOnlyCookieJWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReserveAPIView(GenericAPIView):
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceReserveSerializers

    @swagger_auto_schema(
        operation_description="دریافت اطلاعات یک رزرو بر اساس reserve-id که باید در پارامترهای لینک ارسال شود.",
        responses={
            200: ServiceReserveSerializers,
            400: openapi.Response('درخواست نامعتبر است. reserve-id باید در پارامترهای لینک ارسال شود.'),
            404: openapi.Response('رزرو با این reserve-id پیدا نشد.'),
            403: openapi.Response('شما به این رزرو دسترسی ندارید.')
        },
        manual_parameters=[
            openapi.Parameter('reserve-id', openapi.IN_QUERY, description="شناسه رزرو که باید در پارامترهای لینک ارسال شود.",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        reserve_id = request.query_params.get('reserve-id')

        if not reserve_id:
            is_admin = request.user.role == 'admin'
            if is_admin:

                reserve_list = ServiceReserve.objects()
            else:
                reserve_list = ServiceReserve.objects(user=request.user.phone_number)

            reserver_serializer = self.serializer_class(reserve_list, many=True)
            return JsonResponse({'data':reserver_serializer.data}, status=status.HTTP_200_OK)

        reserve_obj = ServiceReserve.objects(id=reserve_id).first()
        if not reserve_obj:
            return JsonResponse({'message': 'reserve-id does not match'}, status=status.HTTP_404_NOT_FOUND)

        is_admin = request.user.role == 'admin'
        if not is_admin and reserve_obj.user != request.user.phone_number:
            return JsonResponse({'message': 'you can not access to this reserve'},
                                 status=status.HTTP_403_FORBIDDEN)

        reserver_serializer = self.serializer_class(reserve_obj)
        return JsonResponse(reserver_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="ایجاد یک رزرو جدید. برای ادمین‌ها باید شماره موبایل کاربر با کلید 'user' در داده‌های ارسال شده قرار گیرد.",
        responses={
            201: ServiceReserveSerializers,
            400: openapi.Response('شماره تلفن کاربر برای ادمین‌ها الزامی است.'),
            404: openapi.Response('کاربر با این شماره موبایل پیدا نشد.')
        },
        request_body=ServiceReserveSerializers
    )
    def post(self, request):
        is_admin = request.user.role == 'admin'
        phone_number = request.data.get('user') if is_admin else request.user.phone_number

        if is_admin and not phone_number:
            return JsonResponse({'message': 'User phone number is required for admins, send it with the key (user) in post data'},
                                 status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if not user:
            return JsonResponse({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        reserve_obj = ServiceReserve(user=user.phone_number)
        reserve_obj.save()

        reserve_serializer = self.serializer_class(reserve_obj)
        return JsonResponse(reserve_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="به‌روزرسانی مرحله رزرو. باید پارامترهای reserve-id و next-stage را در لینک ارسال کنید.",
        responses={
            200: openapi.Response('رزرو با موفقیت به روز شد.'),
            400: openapi.Response('مرحله رزرو نامعتبر است یا پارامترهای مورد نیاز ارسال نشده است.'),
            403: openapi.Response('شما به این رزرو دسترسی ندارید.'),
            404: openapi.Response('رزرو با این reserve-id پیدا نشد.')
        },
        manual_parameters=[
            openapi.Parameter('reserve-id', openapi.IN_QUERY, description="شناسه رزرو برای به روز رسانی مرحله رزرو.",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('next-stage', openapi.IN_QUERY, description="مقدار Boolean (0 یا 1) برای مشخص کردن که آیا به مرحله بعدی می‌روید یا قبلی.",
                              type=openapi.TYPE_BOOLEAN)
        ]
    )
    def patch(self, request):
        is_admin = request.user.role == 'admin'
        reserve_id = request.query_params.get('reserve-id')

        if not reserve_id:
            return JsonResponse({'message': 'reserve-id is required in links query params'},
                                 status=status.HTTP_400_BAD_REQUEST)

        reserve = ServiceReserve.objects(id=reserve_id).first()
        if not reserve:
            return JsonResponse({'message': 'reserve id not found'}, status=status.HTTP_404_NOT_FOUND)

        if not is_admin and request.user.phone_number != reserve.user:
            return JsonResponse({'message': 'You do not have access to this reserve'}, status=status.HTTP_403_FORBIDDEN)

        next_stage_status = request.query_params.get('next-stage')
        if next_stage_status is None:
            return JsonResponse({'message': "next-stage is required in links query params"},
                                 status=status.HTTP_400_BAD_REQUEST)

        try:
            next_stage_status = bool(int(next_stage_status))  # تبدیل به مقدار بولی
        except ValueError:
            return JsonResponse({'message': "next-stage should be a boolean value (0 or 1)"},
                                 status=status.HTTP_400_BAD_REQUEST)

        if next_stage_status:
            if reserve.stage not in [1, 2, 3, 4, 5]:
                return JsonResponse({'message': "Invalid stage number. Acceptable stages: [1, 2, 3, 4, 5]"},
                                     status=status.HTTP_400_BAD_REQUEST)
            update_status, update_message = reserve.handle_next_stage(request.data)
        else:
            if reserve.stage not in [2, 3, 4]:
                return JsonResponse({'message': "Invalid stage number. Acceptable stages: [2, 3, 4]"},
                                     status=status.HTTP_400_BAD_REQUEST)
            update_status, update_message = reserve.handle_previous_stage(request.data)

        return JsonResponse(update_message, status=status.HTTP_200_OK if update_status else status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="کنسل کردن یک رزرو. باید reserve-id را در لینک ارسال کنید.",
        responses={
            200: openapi.Response('رزرو با موفقیت کنسل شد.'),
            400: openapi.Response('رزرو با این reserve-id پیدا نشد.'),
            403: openapi.Response('شما به این رزرو دسترسی ندارید.')
        },
        manual_parameters=[
            openapi.Parameter('reserve-id', openapi.IN_QUERY, description="شناسه رزرو برای کنسل کردن.",
                              type=openapi.TYPE_STRING)
        ]
    )
    def delete(self, request):
        is_admin = request.user.role == 'admin'
        reserve_id = request.query_params.get('reserve-id')

        if not reserve_id:
            return JsonResponse({'message': 'reserve-id is required in links query params'},
                                 status=status.HTTP_400_BAD_REQUEST)

        reserve = ServiceReserve.objects(id=reserve_id).first()
        if not reserve:
            return JsonResponse({'message': 'reserve id not found'}, status=status.HTTP_404_NOT_FOUND)

        if not is_admin and request.user.phone_number != reserve.user:
            return JsonResponse({'message': 'You do not have access to this reserve'},
                                 status=status.HTTP_403_FORBIDDEN)

        reserve.cancel_reservation()

        return JsonResponse({'message': "Successfully canceled reserve"}, status=status.HTTP_200_OK)
