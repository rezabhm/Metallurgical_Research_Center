from django.db import models


# Create your models here.
class Service(models.Model):

    service_name = models.CharField(max_length=75)
    description = models.TextField()
    price = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='service/cover/')
    is_package = models.BooleanField(default=False)

    def __str__(self):
        return self.service_name


class ServiceImage(models.Model):

    image = models.ImageField(upload_to='service/image/')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service.service_name}@{self.pk}'


class ServiceReservedDate(models.Model):

    reserved_from = models.CharField(max_length=100)
    reserved_to = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service.service_name}@{self.reserved_from}>{self.reserved_to}'
