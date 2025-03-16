from rest_framework import serializers

from apps.users.models import CustomUser


class OTPVerifyCodeSerializers(serializers.Serializer):

    code = serializers.CharField(max_length=6)


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'is_signup', 'phone_number', 'role']
