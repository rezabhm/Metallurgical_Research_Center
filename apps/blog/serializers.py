import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.timezone import now
from rest_framework import serializers

from apps.blog.document import *


class CategorySerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    category_name = serializers.CharField()
    slug = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        blog_list = Blog.objects(category_list__contain=[representation['id']])
        blog_serializers = BlogSerializers(data=blog_list, many=True)
        blog_serializers.is_valid()

        representation['blogs'] = blog_serializers.data

        return representation

    def create(self, validated_data):
        category = Category(**validated_data)
        category.save()
        return category


class BlogSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    cover_image = serializers.CharField()
    category_list = serializers.ListField()
    tags = serializers.ListField()
    slug = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        blog_images = BlogImage.objects(blog=representation['id'])
        blog_images_serializers = BlogImageSerializers(data=blog_images, many=True)
        blog_images_serializers.is_valid()

        representation['blog-image'] = blog_images_serializers.data

        blog_contents = BlogContent.objects(blog=representation['id'])
        blog_contents_serializers = BlogContentSerializers(data=blog_contents, many=True)
        blog_contents_serializers.is_valid()

        representation['blog-content'] = blog_contents_serializers.data

        return representation

    def create(self, validated_data):
        x = Blog(**validated_data)
        x.save()
        return x


class BlogContentSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    index = serializers.IntegerField()
    content = serializers.CharField()
    class_name = serializers.CharField()
    is_multiline = serializers.BooleanField()
    blog = serializers.UUIDField()

    def create(self, validated_data):
        x = BlogContent(**validated_data)
        x.save()
        return x


class BlogImageSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    image = serializers.CharField()
    blog = serializers.UUIDField()

    def create(self, validated_data):
        # گرفتن تصویر از validated_data
        image = validated_data.pop('image')

        # ذخیره تصویر
        file_name = f"{now().strftime('%Y%m%d%H%M%S')}_{image.name}"  # برای ایجاد نام منحصر به فرد
        file_path = os.path.join(settings.MEDIA_ROOT, 'blog_images', file_name)

        # ذخیره تصویر در سیستم فایل
        with default_storage.open(file_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # ساخت URL تصویر
        image_url = os.path.join(settings.MEDIA_URL, 'blog_images', file_name)

        # مسیر URL تصویر را در validated_data اضافه می‌کنیم
        validated_data['image'] = image_url

        blog_image = BlogImage(**validated_data)
        blog_image.save()

        return blog_image
