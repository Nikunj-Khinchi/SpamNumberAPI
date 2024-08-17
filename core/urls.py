from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContactViewSet, SpamReportViewSet, SearchView, UpdateProfileView, VerifyTokenView, FetchProfileView 

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'spam', SpamReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/verify_user/', VerifyTokenView.as_view(), name='verify_user'),
    path('search/', SearchView.as_view(), name='search'),
    path('user/profile/', FetchProfileView.as_view(), name='fetch-profile'),
    path('user/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
]
