from rest_framework import serializers

from apps.reserve.document import ServiceReserve


class ServiceReserveSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    stage = serializers.IntegerField()
    is_canceled = serializers.BooleanField()
    user = serializers.CharField()
    is_package = serializers.BooleanField()

    # stage 1
    reserve_from = serializers.CharField()
    reserve_to = serializers.CharField()
    service = serializers.CharField()

    # stage 2
    is_reservation_time_verified = serializers.BooleanField()
    admin_description = serializers.CharField()
    reserve_duration = serializers.FloatField()
    total_price = serializers.FloatField()

    # stage 3
    payment_image = serializers.CharField()

    # stage 4
    is_payment_verified = serializers.BooleanField()

    # stage 5
    is_finished = serializers.BooleanField()
    report_file = serializers.CharField()

    def update(self, instance, validated_data):

        for key, value in validated_data.items():

            setattr(instance, key, value)

        instance.save()
        return instance
