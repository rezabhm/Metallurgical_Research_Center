from django.core.exceptions import ObjectDoesNotExist

from apps.users.models import CustomUser


def check_user_exist(phone_number):

    """ check user exist or not """
    try:
        return CustomUser.objects.get(phone_number=phone_number)

    except ObjectDoesNotExist:
        return None


def create_user(phone_number):

    """ create new user with given phone number """
    user = CustomUser(

        username=phone_number,
        phone_number=phone_number,
        role='customer'

    )

    user.save()
    return user
