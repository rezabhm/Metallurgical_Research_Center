import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser
from configs.settings.base import verify_limit_time


class OTPSendCodeTestCase(APITestCase):

    def setUp(self):

        # get url name
        self.url = reverse('otp-send-code', kwargs={'phone_number': '09111'})
        self.new_user = CustomUser(username='01', phone_number='09111')
        self.new_user.save()

    def test_send_code_to_exist_user(self):

        # check use exist user or create new user ( this api must use exist user )
        # check generate new code or not ( this api must generate new code )

        user_list = [obj for obj in CustomUser.objects.all()]
        response = self.client.get(self.url)
        new_get_user = CustomUser.objects.get(phone_number='09111')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_list, [self.new_user])
        self.assertNotEqual(new_get_user.otp_code, '000000')

    def test_send_code_to_new_user(self):

        # check use exist user or create new user ( this api must create new user )
        # check generate new code or not ( this api must generate new code )

        url = reverse('otp-send-code', kwargs={'phone_number': '09'})

        old_user_list = [obj for obj in CustomUser.objects.all()]
        response = self.client.get(url)
        new_user_list = [obj for obj in CustomUser.objects.all()]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_user_list, new_user_list)
        self.assertEqual(len(old_user_list)+1, len(new_user_list))
        self.assertNotEqual(new_user_list[-1].otp_code, '000000')


class OTPVerifyCodeTestCase(APITestCase):

    def setUp(self):

        self.url = reverse('otp-verify-code', kwargs={'phone_number':'0911'})

    def test_verify_code(self):

        # check verify code with correct code

        otp_url = reverse('otp-send-code', kwargs={'phone_number': '0911'})
        self.client.get(otp_url)

        user = CustomUser.objects.all()[0]

        response = self.client.post(self.url, data={'code': user.otp_code}, follow='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_wrong_code(self):

        # check verify code with wrong code

        otp_url = reverse('otp-send-code', kwargs={'phone_number': '0911'})
        self.client.get(otp_url)

        response = self.client.post(self.url, data={'code': '21351'}, follow='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_time_limit_exceed_code(self):

        # check verify code with wrong code

        otp_url = reverse('otp-send-code', kwargs={'phone_number': '0911'})
        self.client.get(otp_url)

        # convert minute to seconds and add it with 10 seconds
        time.sleep((verify_limit_time * 60) + 10)

        user = CustomUser.objects.all()[0]

        response = self.client.post(self.url, data={'code': user.otp_code}, follow='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
