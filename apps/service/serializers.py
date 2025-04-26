from rest_framework import serializers

from apps.service.models import *


class ServiceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        service_images = ServiceImage.objects.filter(service=instance)
        service_image_serializers = ServiceImageSerializers(service_images, many=True)
        representation['service-images'] = service_image_serializers.data

        reserve_dates = ServiceReservedDate.objects.filter(service=instance)
        service_reserve_date_serializers = ServiceReserveDateSerializers(reserve_dates, many=True)
        representation['service-reserve_date'] = service_reserve_date_serializers.data

        return representation


class ServiceImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServiceImage
        fields = '__all__'


class ServiceReserveDateSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceReservedDate
        fields = '__all__'
