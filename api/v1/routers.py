from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from api.v1.api_view.authentication_view import *
from api.v1.api_view.blog_view import *
from api.v1.api_view.reserve_view import ReserveAPIView
from api.v1.api_view.service_view import *
from api.v1.api_view.users_view import *
from apps.blog.graphQL_schema import schema

router = DefaultRouter()

""" Users API """
router.register('user/admin', UserAdminAPIView, basename='user-admin')
router.register('user/customer', UserCustomerAPIView, basename='user-customer')

""" Service API """
router.register('service/s/admin', ServiceAdminAPIView, basename='service-admin')
router.register('service/s/customer', ServiceAnyAPIView, basename='service-customer')
router.register('service/images/admin', ServiceImageAdminAPIView, basename='service-images-admin')
router.register('service/images/customer', ServiceImageAnyAPIView, basename='service-images-customer')
router.register('service/reserve-date/admin', ServiceReserveDateAdminAPIView, basename='service-reserve-date-admin')
router.register('service/reserve-date/customer', ServiceReserveDateAnyAPIView, basename='service-reserve-date-customer')

""" Blog API """
router.register('blog/category/admin', CategoryAPIView, basename='admin-category')
router.register('blog/b/admin', BlogAPiView, basename='admin-blog')
router.register('blog/content/admin', BlogContentAPiView, basename='admin-blog-content')
router.register('blog/image/admin', BlogImageAPiView, basename='admin-blog-image')
router.register('blog/b/any', BlogReadAPiView, basename='blog-any')
router.register('blog/c/any', CategoryReadAPIView, basename='category-any')

urlpatterns = router.urls
urlpatterns += [

    path(r'authentication/otp/send-code/<str:phone_number>/', OTPSendCodeAPIView.as_view(), name='otp-send-code'),
    path(r'authentication/otp/verify-code/<str:phone_number>/', OTPVerifyCodeAPIView.as_view(), name='otp-verify-code'),
    path(r'reserve', ReserveAPIView.as_view(), name='reserve'),

    path("graphql/blogs", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]


