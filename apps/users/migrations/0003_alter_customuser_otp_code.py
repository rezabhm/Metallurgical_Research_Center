# Generated by Django 5.1.6 on 2025-03-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_otp_code_customuser_otp_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='otp_code',
            field=models.CharField(default='00000', max_length=6),
        ),
    ]
