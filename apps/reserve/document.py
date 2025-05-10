import os

import mongoengine as mongo
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def check_validated_data(stage, validated_data):
    stage_key_handler = {

        '1': ['reserve_from', 'reserve_to', 'service'],
        '2': ['is_reservation_time_verified', 'admin_description', 'reserve_duration', 'total_price'],
        '3': ['payment_image'],
        '4': ['is_payment_verified'],
        '5': ['is_finished'],

    }

    if list(validated_data.keys()) != stage_key_handler[str(stage)]:
        return False, {'message': f'you didnt send keys > {stage_key_handler[str(stage)]}'}

    return True, {}


class ServiceReserve(mongo.Document):

    stage = mongo.IntField(default=1)
    is_canceled = mongo.BooleanField(default=False)
    user = mongo.StringField(default='')
    admin_description = mongo.StringField(default='')

    # stage 1
    reserve_from = mongo.StringField(default='')
    reserve_to = mongo.StringField(default='')
    service = mongo.StringField(default='')

    # stage 2
    is_reservation_time_verified = mongo.BooleanField(default=False)
    reserve_duration = mongo.FloatField(default=0.0)
    total_price = mongo.FloatField(default=0.0)

    # stage 3
    payment_image = mongo.StringField(required=False)

    # stage 4
    is_payment_verified = mongo.BooleanField(default=False)

    # stage 5
    is_finished = mongo.BooleanField(default=False)

    meta = {'collection': 'ServiceReserve'}

    def handle_previous_stage(self, validated_data):
        stage_handler = {

            '2': self.pre_stage_2,
            '3': self.pre_stage_3,
            '4': self.pre_stage_4,

        }
        return stage_handler[str(self.stage)](validated_data)

    def handle_next_stage(self, validated_data):

        stage_handler = {

            '1': self.next_stage_1,
            '2': self.next_stage_2,
            '3': self.next_stage_3,
            '4': self.next_stage_4,
            '5': self.next_stage_5,

        }

        check_status, check_data = check_validated_data(self.stage, validated_data)

        if not check_status:
            return False, check_data

        return stage_handler[str(self.stage)](validated_data)

    def next_stage_1(self, validated_data):

        self.reserve_from = validated_data['reserve_from']
        self.reserve_to = validated_data['reserve_to']
        self.service = validated_data['service']

        self.save()
        self.next_stage()

        return True, validated_data

    def next_stage_2(self, validated_data):

        self.is_reservation_time_verified = validated_data['is_reservation_time_verified']
        self.admin_description = validated_data['admin_description']
        self.reserve_duration = validated_data['reserve_duration']
        self.total_price = validated_data['total_price']

        self.save()
        self.next_stage()

        return True, validated_data


    def next_stage_3(self, validated_data):
        # دریافت عکس از داده‌های ورودی
        payment_image = validated_data['payment_image']

        # ایجاد نام فایل جدید برای عکس (می‌توانید نام فایل را به دلخواه تغییر دهید)
        file_name = f'payment_images/{self.id}_{os.path.basename(payment_image.name)}'

        # ذخیره عکس در دایرکتوری مناسب (در اینجا از default_storage استفاده می‌کنیم)
        file_path = default_storage.save(file_name, ContentFile(payment_image.read()))

        # ذخیره مسیر فایل در فیلد payment_image
        self.payment_image = file_path

        validated_data['payment_image'] = file_path

        # ذخیره تغییرات در مدل
        self.save()

        # مرحله بعدی
        self.next_stage()

        return True, validated_data

    def next_stage_4(self, validated_data):
        self.is_payment_verified = validated_data['is_payment_verified']

        self.save()
        self.next_stage()

        return True, validated_data

    def next_stage_5(self, validated_data):
        self.is_finished = validated_data['is_finished']

        self.save()
        self.next_stage()

        return True, validated_data

    def pre_stage_2(self, validated_data):
        self.reserve_from = ''
        self.reserve_to = ''
        self.service = validated_data['service']
        self.is_reservation_time_verified = False
        self.admin_description = validated_data['admin_description']
        self.reserve_duration = 0.0
        self.total_price = 0.0

        self.save()
        self.previous_stage()

        return True, validated_data

    def pre_stage_3(self, validated_data):
        self.payment_image = ''
        self.stage = 1
        self.is_reservation_time_verified = False
        self.admin_description = ''
        self.reserve_duration = 0.0
        self.total_price = 0.0

        self.save()

        return True, validated_data

    def pre_stage_4(self, validated_data):
        self.admin_description = validated_data['admin_description']
        self.payment_image = ''
        self.is_payment_verified = False

        self.save()
        self.previous_stage()

        return True, validated_data

    def next_stage(self):
        self.stage += 1
        self.save()

    def previous_stage(self):
        self.stage -= 1
        self.save()

    def verify_reservation_time(self):
        self.is_reservation_time_verified = True
        self.save()

    def verify_payment(self):
        self.is_payment_verified = True
        self.save()

    def finish_reserve(self):
        self.is_finished = True
        self.save()

    def cancel_reservation(self):
        self.is_canceled = True
        self.save()