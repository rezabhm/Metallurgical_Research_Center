import os
import random

from django.conf import settings
from django.core.files.base import ContentFile
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

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


class BlogSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    cover_image = serializers.ImageField()
    category_list = serializers.ListField()
    tags = serializers.ListField()
    slug = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # ✅ تبدیل category_list از DBRef به id یا نام
        if hasattr(instance, 'category_list') and instance.category_list:
            representation['category_list'] = [
                str(category.id) for category in instance.category_list
            ]

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

        # گرفتن تصویر از validated_data
        image = validated_data.pop('cover_image')

        # ایجاد نام فایل جدید برای عکس (می‌توانید نام فایل را به دلخواه تغییر دهید)
        file_name = f'cover_image/{str(random.randint(0,100000))}-{os.path.basename(image.name)}'

        # ذخیره عکس در دایرکتوری مناسب (در اینجا از default_storage استفاده می‌کنیم)
        file_path = default_storage.save(file_name, ContentFile(image.read()))

        validated_data['cover_image'] = file_path

        x = Blog(**validated_data)
        x.save()
        return x

    def update(self, instance, validated_data):
        if 'cover_image' in validated_data:
            # گرفتن تصویر از validated_data
            image = validated_data.get('cover_image', instance.cover_image)

            # ایجاد نام فایل جدید برای عکس (می‌توانید نام فایل را به دلخواه تغییر دهید)
            file_name = f'cover_image/{str(random.randint(0,100000))}-{os.path.basename(image.name)}'

            # ذخیره عکس در دایرکتوری مناسب (در اینجا از default_storage استفاده می‌کنیم)
            file_path = default_storage.save(file_name, ContentFile(image.read()))

            validated_data['cover_image'] = file_path

        instance.title = validated_data.get('title', instance.title)
        instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        instance.category_list = validated_data.get('category_list', instance.category_list)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


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

    def update(self, instance, validated_data):
        instance.index = validated_data.get('index', instance.index)
        instance.content = validated_data.get('content', instance.content)
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.is_multiline = validated_data.get('is_multiline', instance.is_multiline)
        instance.blog = validated_data.get('blog', instance.blog)
        instance.save()
        return instance


class BlogImageSerializers(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    image = serializers.ImageField()
    blog = serializers.UUIDField()

    def create(self, validated_data):
        # گرفتن تصویر از validated_data
        image = validated_data.pop('image')

        # ایجاد نام فایل جدید برای عکس (می‌توانید نام فایل را به دلخواه تغییر دهید)
        file_name = f'blog_images/{str(random.randint(0,100000))}-{os.path.basename(image.name)}'

        # ذخیره عکس در دایرکتوری مناسب (در اینجا از default_storage استفاده می‌کنیم)
        file_path = default_storage.save(file_name, ContentFile(image.read()))

        validated_data['image'] = file_path

        blog_image = BlogImage(**validated_data)
        blog_image.save()

        return blog_image

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.blog = validated_data.get('blog', instance.blog)
        instance.save()
        return instance
