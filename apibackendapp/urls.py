# DefaultRouter is a class that automatically creates URLS for Viewsets
from rest_framework.routers import DefaultRouter
from .import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register(r'employees',views.EmployeeViewSet)
router.register(r'departments',views.DepartmentViewSet)
router.register(r'projects',views.ProjectViewSet)

#SignupAPIView is an APIView, not a viewset
urlpatterns=[
    path("signup/",views.SignupAPIView.as_view(),name='user-signup'),
    path("login/",views.LoginAPIView.as_view(),name='user-login'),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]

urlpatterns+=router.urls
