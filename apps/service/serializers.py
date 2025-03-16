from rest_framework import serializers

from apps.service.models import *


class ServiceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        service_image_serializers = ServiceImageSerializers(data=ServiceImage.objects.filter(service__id=representation['pk']), many=True)
        service_image_serializers.is_valid()
        representation['service-images'] = service_image_serializers.data

        service_reserve_date_serializers = ServiceReserveDateSerializers(data=ServiceReservedDate.objects.filter(service__id=representation['pk']), many=True)
        service_reserve_date_serializers.is_valid()
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
