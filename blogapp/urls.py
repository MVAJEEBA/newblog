from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, RegisterView, LoginView

# Create a router and register our BlogPost viewset with it.
router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
