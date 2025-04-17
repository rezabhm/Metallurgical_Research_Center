# from rest_framework.permissions import IsAdminUser, AllowAny
# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from apps.blog.document import *
# from apps.blog.serializers import *
# from configs.authentication import HTTPOnlyCookieJWTAuthentication
#
#
# class CategoryAPIView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.CreateModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [IsAdminUser]
#     serializer_class = CategorySerializers
#     queryset = Category.objects()
#
#
# class BlogAPiView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.CreateModelMixin,
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [IsAdminUser]
#     serializer_class = BlogSerializers
#     queryset = Blog.objects()
#
#
# class BlogImageAPiView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.CreateModelMixin,
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [IsAdminUser]
#     serializer_class = BlogImageSerializers
#     queryset = BlogImage.objects()
#
#
# class BlogContentAPiView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.CreateModelMixin,
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [IsAdminUser]
#     serializer_class = BlogContentSerializers
#     queryset = BlogContent.objects()
#
#
# class CategoryReadAPIView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = CategorySerializers
#     queryset = Category.objects()
#
#
# class BlogReadAPiView(
#
#     GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#
#     ):
#
#     authentication_classes = [HTTPOnlyCookieJWTAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = BlogSerializers
#     queryset = Blog.objects()

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.blog.document import *
from apps.blog.serializers import *
from configs.authentication import HTTPOnlyCookieJWTAuthentication


class CategoryAPIView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    این کلاس برای مدیریت دسته‌بندی‌ها استفاده می‌شود. کاربران با دسترسی مدیر (Admin) قادر به
    مشاهده، ایجاد، به‌روزرسانی و حذف دسته‌بندی‌ها خواهند بود.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializers
    queryset = Category.objects()
    lookup_field = 'id'  # فیلد مورد استفاده برای جستجو
    slug_field = 'slug'  # فیلد اسلاگ برای URL

    @swagger_auto_schema(
        operation_summary="لیست، ایجاد، به‌روزرسانی و حذف دسته‌بندی‌ها",
        operation_description="این API برای مدیریت دسته‌بندی‌ها است. برای دریافت لیست، ایجاد، ویرایش و حذف دسته‌بندی‌ها استفاده می‌شود. تنها مدیران دسترسی دارند.",
        responses={
            200: CategorySerializers,
            201: CategorySerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
            404: openapi.Response('دسته‌بندی پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="صفحه مورد نظر برای دریافت لیست دسته‌بندی‌ها", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="تعداد دسته‌بندی‌ها در هر صفحه", type=openapi.TYPE_INTEGER)
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام دسته‌بندی‌ها.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک دسته‌بندی خاص",
        operation_description="برای دریافت اطلاعات یک دسته‌بندی خاص باید از فیلد 'id' یا 'slug' استفاده کنید. اگر از اسلاگ استفاده می‌کنید، از پارامتر slug در URL استفاده کنید.",
        responses={
            200: CategorySerializers,
            404: openapi.Response('دسته‌بندی پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک دسته‌بندی خاص.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد یک دسته‌بندی جدید",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. در درخواست باید اطلاعات دسته‌بندی جدید ارسال شود.",
        request_body=CategorySerializers,
        responses={
            201: CategorySerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        برای ایجاد یک دسته‌بندی جدید.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی یک دسته‌بندی موجود",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. برای به‌روزرسانی دسته‌بندی، شناسه یا اسلاگ آن باید در URL مشخص شود.",
        request_body=CategorySerializers,
        responses={
            200: CategorySerializers,
            404: openapi.Response('دسته‌بندی پیدا نشد.'),
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def update(self, request, *args, **kwargs):
        """
        برای به‌روزرسانی یک دسته‌بندی موجود.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف یک دسته‌بندی",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. باید شناسه یا اسلاگ دسته‌بندی مشخص شود.",
        responses={
            200: openapi.Response('دسته‌بندی با موفقیت حذف شد.'),
            404: openapi.Response('دسته‌بندی پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        برای حذف یک دسته‌بندی.
        """
        return super().destroy(request, *args, **kwargs)


class BlogAPIView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin
):
    """
    این کلاس برای مدیریت مطالب بلاگ استفاده می‌شود. عملیات‌های مختلفی شامل دریافت، ایجاد،
    به‌روزرسانی و حذف مطالب بلاگ توسط کاربران با دسترسی مدیر (Admin) قابل انجام است.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogSerializers
    queryset = Blog.objects()
    lookup_field = 'id'
    slug_field = 'slug'

    @swagger_auto_schema(
        operation_summary="لیست، ایجاد، به‌روزرسانی و حذف مطالب بلاگ",
        operation_description="این API برای مدیریت مطالب بلاگ است. برای دریافت لیست، ایجاد، ویرایش و حذف مطالب بلاگ استفاده می‌شود. تنها مدیران دسترسی دارند.",
        responses={
            200: BlogSerializers,
            201: BlogSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
            404: openapi.Response('مطالب بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="صفحه مورد نظر برای دریافت لیست مطالب بلاگ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="تعداد مطالب بلاگ در هر صفحه", type=openapi.TYPE_INTEGER)
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام مطالب بلاگ.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک مطلب بلاگ خاص",
        operation_description="برای دریافت اطلاعات یک مطلب بلاگ خاص، باید از 'id' یا 'slug' استفاده کنید.",
        responses={
            200: BlogSerializers,
            404: openapi.Response('مطلب بلاگ پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک مطلب بلاگ خاص.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد یک مطلب بلاگ جدید",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. در درخواست باید اطلاعات مطلب بلاگ جدید ارسال شود.",
        request_body=BlogSerializers,
        responses={
            201: BlogSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        برای ایجاد یک مطلب بلاگ جدید.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی یک مطلب بلاگ موجود",
        operation_description="برای به‌روزرسانی یک مطلب بلاگ، شناسه یا اسلاگ آن باید در URL مشخص شود.",
        request_body=BlogSerializers,
        responses={
            200: BlogSerializers,
            404: openapi.Response('مطلب بلاگ پیدا نشد.'),
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def update(self, request, *args, **kwargs):
        """
        برای به‌روزرسانی یک مطلب بلاگ موجود.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف یک مطلب بلاگ",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. باید شناسه یا اسلاگ مطلب بلاگ مشخص شود.",
        responses={
            200: openapi.Response('مطلب بلاگ با موفقیت حذف شد.'),
            404: openapi.Response('مطلب بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        برای حذف یک مطلب بلاگ.
        """
        return super().destroy(request, *args, **kwargs)

class BlogImageAPiView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin
):
    """
    این کلاس برای مدیریت تصاویر بلاگ است. عملیات‌های مختلف شامل مشاهده، ایجاد،
    به‌روزرسانی و حذف تصاویر بلاگ توسط کاربران با دسترسی مدیر (Admin) انجام می‌شود.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogImageSerializers
    queryset = BlogImage.objects()

    @swagger_auto_schema(
        operation_summary="لیست، ایجاد، به‌روزرسانی و حذف تصاویر بلاگ",
        operation_description="این API برای مدیریت تصاویر بلاگ است. برای دریافت لیست، ایجاد، ویرایش و حذف تصاویر بلاگ استفاده می‌شود. تنها مدیران دسترسی دارند.",
        responses={
            200: BlogImageSerializers,
            201: BlogImageSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
            404: openapi.Response('تصویر بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام تصاویر بلاگ.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک تصویر بلاگ خاص",
        operation_description="برای دریافت اطلاعات یک تصویر بلاگ خاص، باید از 'id' یا 'slug' استفاده کنید. اگر از اسلاگ استفاده می‌کنید، از پارامتر slug در URL استفاده کنید.",
        responses={
            200: BlogImageSerializers,
            404: openapi.Response('تصویر بلاگ پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک تصویر بلاگ خاص.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد یک تصویر بلاگ جدید",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. در درخواست باید اطلاعات تصویر بلاگ جدید ارسال شود.",
        request_body=BlogImageSerializers,
        responses={
            201: BlogImageSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        برای ایجاد یک تصویر بلاگ جدید.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی یک تصویر بلاگ",
        operation_description="برای به‌روزرسانی یک تصویر بلاگ، شناسه یا اسلاگ آن باید در URL مشخص شود.",
        request_body=BlogImageSerializers,
        responses={
            200: BlogImageSerializers,
            404: openapi.Response('تصویر بلاگ پیدا نشد.'),
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def update(self, request, *args, **kwargs):
        """
        برای به‌روزرسانی یک تصویر بلاگ موجود.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف یک تصویر بلاگ",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. باید شناسه یا اسلاگ تصویر بلاگ مشخص شود.",
        responses={
            200: openapi.Response('تصویر بلاگ با موفقیت حذف شد.'),
            404: openapi.Response('تصویر بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        برای حذف یک تصویر بلاگ.
        """
        return super().destroy(request, *args, **kwargs)


class BlogContentAPIView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin
):
    """
    این کلاس برای مدیریت محتوای بلاگ استفاده می‌شود. کاربران با دسترسی مدیر می‌توانند
    محتوای بلاگ را مشاهده، ایجاد، به‌روزرسانی و حذف کنند.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BlogContentSerializers
    queryset = BlogContent.objects()

    @swagger_auto_schema(
        operation_summary="لیست، ایجاد، به‌روزرسانی و حذف محتوای بلاگ",
        operation_description="این API برای مدیریت محتوای بلاگ است. برای دریافت لیست، ایجاد، ویرایش و حذف محتوای بلاگ استفاده می‌شود. تنها مدیران دسترسی دارند.",
        responses={
            200: BlogContentSerializers,
            201: BlogContentSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
            404: openapi.Response('محتوا بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام محتواهای بلاگ.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک محتوای بلاگ خاص",
        operation_description="برای دریافت اطلاعات یک محتوای بلاگ خاص، باید از 'id' یا 'slug' استفاده کنید.",
        responses={
            200: BlogContentSerializers,
            404: openapi.Response('محتوا بلاگ پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک محتوای بلاگ خاص.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="ایجاد یک محتوای بلاگ جدید",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. در درخواست باید اطلاعات محتوای بلاگ جدید ارسال شود.",
        request_body=BlogContentSerializers,
        responses={
            201: BlogContentSerializers,
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        برای ایجاد یک محتوای بلاگ جدید.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="به‌روزرسانی یک محتوای بلاگ",
        operation_description="برای به‌روزرسانی یک محتوای بلاگ، شناسه یا اسلاگ آن باید در URL مشخص شود.",
        request_body=BlogContentSerializers,
        responses={
            200: BlogContentSerializers,
            404: openapi.Response('محتوا بلاگ پیدا نشد.'),
            400: openapi.Response('درخواست نامعتبر است.'),
        }
    )
    def update(self, request, *args, **kwargs):
        """
        برای به‌روزرسانی یک محتوای بلاگ موجود.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="حذف یک محتوای بلاگ",
        operation_description="فقط مدیران می‌توانند این عملیات را انجام دهند. باید شناسه یا اسلاگ محتوای بلاگ مشخص شود.",
        responses={
            200: openapi.Response('محتوا بلاگ با موفقیت حذف شد.'),
            404: openapi.Response('محتوا بلاگ پیدا نشد.'),
            403: openapi.Response('شما دسترسی به این عملیات ندارید.')
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        برای حذف یک محتوای بلاگ.
        """
        return super().destroy(request, *args, **kwargs)


class CategoryReadAPIView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    این کلاس برای مشاهده دسته‌بندی‌ها استفاده می‌شود. دسترسی به این API برای همه کاربران آزاد است.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CategorySerializers
    queryset = Category.objects()

    @swagger_auto_schema(
        operation_summary="دریافت لیست تمام دسته‌بندی‌ها",
        operation_description="این API برای مشاهده لیست تمام دسته‌بندی‌ها است. دسترسی به این API برای همه کاربران آزاد است.",
        responses={
            200: CategorySerializers,
        }
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام دسته‌بندی‌ها.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک دسته‌بندی خاص",
        operation_description="برای دریافت اطلاعات یک دسته‌بندی خاص باید از 'id' یا 'slug' استفاده کنید.",
        responses={
            200: CategorySerializers,
            404: openapi.Response('دسته‌بندی پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک دسته‌بندی خاص.
        """
        return super().retrieve(request, *args, **kwargs)


class BlogReadAPiView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    این کلاس برای مشاهده مطالب بلاگ استفاده می‌شود. دسترسی به این API برای همه کاربران آزاد است.
    """
    authentication_classes = [HTTPOnlyCookieJWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = BlogSerializers
    queryset = Blog.objects()

    @swagger_auto_schema(
        operation_summary="دریافت لیست تمام مطالب بلاگ",
        operation_description="این API برای مشاهده لیست تمام مطالب بلاگ است. دسترسی به این API برای همه کاربران آزاد است.",
        responses={
            200: BlogSerializers,
        }
    )
    def list(self, request, *args, **kwargs):
        """
        برای دریافت لیست تمام مطالب بلاگ.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات یک مطلب بلاگ خاص",
        operation_description="برای دریافت اطلاعات یک مطلب بلاگ خاص باید از 'id' یا 'slug' استفاده کنید.",
        responses={
            200: BlogSerializers,
            404: openapi.Response('مطلب بلاگ پیدا نشد.')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        برای دریافت اطلاعات یک مطلب بلاگ خاص.
        """
        return super().retrieve(request, *args, **kwargs)
